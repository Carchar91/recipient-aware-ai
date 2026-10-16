#!/usr/bin/env python3
"""Owner-authorized handoff only: NEW PRIVATE repository and DRAFT release.

Dry-run by default. Never touches the website, makes a repo public, or selects a license.
Existing remote repositories require separate inspection and are not overwritten.
"""
from pathlib import Path
import argparse,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.package_release import source_files
OWNER='Carchar91';REPO=OWNER+'/recipient-aware-ai'

def run(args,*,check=True,cwd=ROOT):
    r=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
    if check and r.returncode:raise RuntimeError(f'{args[0]} command failed; no automatic retry. {r.stderr.strip()}')
    return r

def main():
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');a=p.parse_args()
    version=(ROOT/'VERSION').read_text().strip();tag='v'+version
    plan={'repository':REPO,'visibility':'private','release':tag,'release_state':'draft_prerelease',
      'website_changes':False,'public_license_selection':False,'live_model_calls':False,'execute':a.execute}
    if not a.execute:print(json.dumps(plan,indent=2));return 0
    for tool in ('git','gh'):
        if not shutil.which(tool):raise RuntimeError(f'{tool} is not installed or not in PATH. No remote action performed.')
    # Refuse to operate inside any existing Git worktree, including a parent website repo.
    probe=run(['git','rev-parse','--show-toplevel'],check=False)
    if probe.returncode==0 or (ROOT/'.git').exists():
        raise RuntimeError('Existing Git worktree detected. Use a fresh standalone extraction; never overwrite or reuse the website worktree.')
    user=run(['gh','api','user','--jq','.login']).stdout.strip()
    if user!=OWNER:raise RuntimeError('Authenticated GitHub owner mismatch. No repository created.')
    for key in ('user.name','user.email'):
        if not run(['git','config','--get',key],check=False).stdout.strip():
            raise RuntimeError('Git author identity is not configured. Configure it locally; never fabricate an identity.')
    exists=run(['gh','repo','view',REPO,'--json','nameWithOwner,visibility'],check=False)
    if exists.returncode==0:raise RuntimeError('Repository already accessible. Stop for review rather than overwrite it.')
    # A failed lookup is ambiguous. Creation will fail safely if a repo exists but is inaccessible.
    run([sys.executable,'tools/verify_manifest.py'])
    verified_manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    with tempfile.TemporaryDirectory() as temp:
        run([sys.executable,'tools/verify.py','--report',str(Path(temp)/'verification.json')])
    listed={row['path'] for row in verified_manifest['files']}
    selected={path.relative_to(ROOT).as_posix() for path in source_files(ROOT)}
    if selected!=listed:
        raise RuntimeError('Release source inventory differs from the verified manifest. '
                           f'Unlisted: {sorted(selected-listed)}; missing or excluded: {sorted(listed-selected)}. '
                           'No repository created.')
    run([sys.executable,'tools/package_release.py'])
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    paths=[x['path'] for x in manifest['files']]+['MANIFEST.json']
    run(['git','init','--initial-branch=main'])
    run(['git','add','--',*paths])
    run(['git','commit','-m',f'Prepare private Recipient-Aware AI {version} candidate'])
    sha=run(['git','rev-parse','HEAD']).stdout.strip()
    run(['git','tag','-a',tag,'-m',f'Private review candidate {version}; no public efficacy claim'])
    # Creation and all following writes are restricted to this NEW methodology repository.
    run(['gh','repo','create',REPO,'--private','--source',str(ROOT),'--remote','origin','--push',
         '--description','Five independent communication protocols with executable contracts and synthetic evaluations',
         '--homepage','https://prudchenko.com/writing/five-communication-protocols'])
    run(['git','push','origin',tag])
    run(['gh','release','create',tag,'--repo',REPO,'--draft','--prerelease','--verify-tag','--latest=false',
         '--title',f'Recipient-Aware AI {version} | Private review',
         '--notes-file','RELEASE_NOTES.md',f'dist/recipient-aware-ai-{version}.zip',
         f'dist/recipient-aware-ai-skills-{version}.zip','dist/SHA256SUMS.txt'])
    remote=json.loads(run(['gh','repo','view',REPO,'--json','nameWithOwner,visibility,url']).stdout)
    release=json.loads(run(['gh','release','view',tag,'--repo',REPO,'--json','url,isDraft,isPrerelease,tagName']).stdout)
    if (remote.get('nameWithOwner')!=REPO or remote.get('visibility')!='PRIVATE'
            or release.get('isDraft') is not True or release.get('isPrerelease') is not True
            or release.get('tagName')!=tag):
        raise RuntimeError('Unexpected final repository identity, visibility or release state. Stop and report; do not attempt automatic changes.')
    print(json.dumps({'repository':remote,'release':release,'commit':sha,'website_changed':False},indent=2))
    return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (RuntimeError,OSError,ValueError,KeyError) as e:
        print(str(e)+'\nIf a remote operation partially succeeded, inspect it before retrying. No deletion, visibility change or overwrite is automatic.',file=sys.stderr)
        raise SystemExit(2)
