import contextlib,hashlib,io,json,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest import mock
from tools import publish_private_draft as publisher
from tools.package_release import archive,source_files
from tools.verify_manifest import verify
from rai.core import ROOT

class PackagingTests(unittest.TestCase):
    def test_archives_are_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.zip';b=Path(d)/'b.zip';items=[('z.txt',b'Z'),('a.txt',b'A')]
            archive(a,items);archive(b,list(reversed(items)));self.assertEqual(a.read_bytes(),b.read_bytes())
    def test_runtime_files_are_excluded(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'README.md').write_text('ok');(root/'runs').mkdir();(root/'runs/private.json').write_text('private')
            self.assertEqual([x.name for x in source_files(root)],['README.md'])
    def test_environment_file_blocks_packaging(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'.env').write_text('not-a-real-secret')
            with self.assertRaises(ValueError):source_files(root)
    def test_manifest_checks_mutations(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'a.txt').write_text('a');m={'files':[{'path':'a.txt','bytes':1,'sha256':hashlib.sha256(b'a').hexdigest()}]}
            (root/'MANIFEST.json').write_text(json.dumps(m));self.assertEqual(verify(root)['status'],'PASS');(root/'a.txt').write_text('b');self.assertEqual(verify(root)['status'],'FAIL')
    def test_manifest_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'MANIFEST.json').write_text(json.dumps({'files':[{'path':'../outside','bytes':0,'sha256':'0'*64}]}))
            self.assertEqual(verify(root)['status'],'FAIL')
    def test_publishing_defaults_private_draft_without_execution(self):
        r=subprocess.run([sys.executable,str(ROOT/'tools/publish_private_draft.py')],capture_output=True,text=True,cwd=ROOT)
        self.assertEqual(r.returncode,0,r.stderr);p=json.loads(r.stdout);self.assertEqual(p['visibility'],'private');self.assertEqual(p['release_state'],'draft_prerelease');self.assertFalse(p['execute'])
    def test_manual_ci_has_no_credentials_or_api_tests(self):
        text=(ROOT/'.github/workflows/offline-verification.yml').read_text();self.assertIn('workflow_dispatch:',text);self.assertNotIn('${{ secrets.',text);self.assertNotIn('live_eval.py',text)

class PublisherSafetyTests(unittest.TestCase):
    """Exercise publication gates with every subprocess mocked; never contact GitHub."""
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name);self.commands=[]
        (self.root/'VERSION').write_text('0.1.0-rc.1')
        (self.root/'README.md').write_text('Synthetic publisher fixture.')
        manifest={'files':[{'path':p.name,'bytes':p.stat().st_size,
                           'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                          for p in sorted(self.root.iterdir())]}
        (self.root/'MANIFEST.json').write_text(json.dumps(manifest))
        self.remote={'nameWithOwner':publisher.REPO,'visibility':'PRIVATE','url':'https://example.invalid/repo'}
        self.release={'isDraft':True,'isPrerelease':True,'tagName':'v0.1.0-rc.1',
                      'url':'https://example.invalid/release'}
        for patch in (mock.patch.object(publisher,'ROOT',self.root),
                      mock.patch.object(publisher.shutil,'which',return_value='/mock/tool'),
                      mock.patch.object(publisher,'run',side_effect=self.fake_run),
                      mock.patch.object(sys,'argv',['publish_private_draft.py','--execute'])):
            patch.start();self.addCleanup(patch.stop)

    def fake_run(self,args,**kwargs):
        self.commands.append(list(args));stdout='';code=0
        if args[:3]==['git','rev-parse','--show-toplevel']:code=1
        elif args[:3]==['gh','api','user']:stdout=publisher.OWNER
        elif args[:3]==['git','config','--get']:stdout='Synthetic test identity'
        elif args[:3]==['gh','repo','view']:
            if args[-1]=='nameWithOwner,visibility':code=1
            else:stdout=json.dumps(self.remote)
        elif args[:3]==['gh','release','view']:stdout=json.dumps(self.release)
        elif args[:3]==['git','rev-parse','HEAD']:stdout='a'*40
        elif args[1:]==['tools/verify_manifest.py']:
            if verify(self.root)['status']!='PASS':raise RuntimeError('Synthetic manifest verification failed.')
        return subprocess.CompletedProcess(args,code,stdout,'')

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()):return publisher.main()

    def test_verified_inventory_and_expected_private_draft_pass(self):
        self.assertEqual(self.execute(),0)
        create=next(args for args in self.commands if args[:3]==['gh','release','create'])
        self.assertIn('--draft',create);self.assertIn('--prerelease',create)

    def test_unlisted_source_stops_before_packaging_or_git_init(self):
        (self.root/'private-note.txt').write_text('Synthetic fixture, no confidential data.')
        with self.assertRaisesRegex(RuntimeError,'Unlisted:.*private-note.txt'):self.execute()
        self.assertFalse(any('tools/package_release.py' in args or args[:2]==['git','init']
                             or args[:3]==['gh','repo','create'] for args in self.commands))

    def test_source_disappearing_after_verification_stops_before_packaging(self):
        original=self.fake_run
        def remove_after_tests(args,**kwargs):
            result=original(args,**kwargs)
            if args[1:2]==['tools/verify.py']:(self.root/'README.md').unlink()
            return result
        with mock.patch.object(publisher,'run',side_effect=remove_after_tests):
            with self.assertRaisesRegex(RuntimeError,'missing or excluded:.*README.md'):self.execute()
        self.assertFalse(any('tools/package_release.py' in args or args[:2]==['git','init']
                             for args in self.commands))

    def test_unexpected_final_repository_or_release_state_fails(self):
        changes=((self.remote,'nameWithOwner','Other/recipient-aware-ai'),
                 (self.remote,'visibility','PUBLIC'),(self.release,'isDraft',False),
                 (self.release,'isPrerelease',False),(self.release,'tagName','vWRONG'),
                 (self.release,'isDraft','true'),(self.release,'isPrerelease','true'))
        for target,key,value in changes:
            with self.subTest(field=key,value=value):
                original=target[key];target[key]=value
                try:
                    with self.assertRaisesRegex(RuntimeError,'Unexpected final'):self.execute()
                finally:target[key]=original
