"""Offline renderer and preservation checks; no model executions."""
import copy
import subprocess
import sys
import unittest
from rai.core import ROOT, NOTICE, load_json, render_output


def pair(cid):
    folder=ROOT/'development/rc2'/cid
    return load_json(folder/'input.json'), load_json(folder/'authored-output.json')


class TargetedFixTests(unittest.TestCase):
    def test_russian_cli_and_development_export_use_identical_renderer(self):
        for case in load_json(ROOT/'development/rc2/cases.json'):
            with self.subTest(case=case['case_id']):
                folder=ROOT/'development/rc2'/case['case_id']
                d,o=pair(case['case_id'])
                cli=subprocess.run([sys.executable,'-m','rai','render','--input',str(folder/'input.json'),
                                    '--output',str(folder/'authored-output.json')],cwd=ROOT,capture_output=True,text=True)
                self.assertEqual(cli.returncode,0,cli.stderr)
                self.assertEqual(cli.stdout,render_output(d,o))
                self.assertTrue((folder/'readable.md').read_text().endswith(cli.stdout))
        d,o=pair('dev-pf-audit');text=render_output(d,o)
        for heading in ('Карта решения','Главный барьер','Рамка общения','Наблюдения'):
            self.assertIn('## '+heading,text)
        self.assertNotIn('## Decision map',text)

    def test_english_quote_inside_russian_response_is_preserved(self):
        d,o=pair('dev-pf-sparse')
        quote='The clerk said: "## Decision map; Alternative: Check: Blocked S2 Source: original words."'
        d['evidence'][0]['text']=quote
        o['evidence_used'][0]['quote']=quote
        o['result']['observations'][0]['observation']=quote
        before=copy.deepcopy((d,o))
        text=render_output(d,o)
        self.assertIn('## Наблюдения',text)
        self.assertIn(quote,text)
        self.assertEqual((d,o),before)
        self.assertIn(NOTICE,text)

    def test_render_never_globally_translates_deliverable_content(self):
        literal='## Decision map\nAlternative: Check: Blocked original Source: [unresolved]'
        for cid,key in [('dev-pp-audit','message'),('dev-dh-sequence','body'),
                        ('dev-rv-sequence','revised_message'),('dev-rl-ready','message')]:
            with self.subTest(case=cid):
                d,o=pair(cid);o['result'][key]+='\n\n'+literal
                self.assertIn(literal,render_output(d,o))

    def test_human_blocker_describes_result_while_audit_retains_step_ids(self):
        d,o=pair('dev-rl-gap');before=copy.deepcopy(o)
        text=render_output(d,o);audit=render_output(d,o,audit=True)
        self.assertNotIn('S2',o['result']['message'])
        self.assertNotIn('S1',text);self.assertNotIn('S2',text)
        self.assertIn('Заблокирован ожидаемый результат (Мария)',text)
        self.assertIn(o['result']['steps'][1]['output'],text)
        self.assertEqual(o['result']['blockers'][0]['blocked_step'],'S2')
        self.assertEqual(o['result']['steps'][1]['depends_on'],['S1'])
        self.assertIn('"blocked_step": "S2"',audit)
        self.assertIn('"depends_on": [',audit)
        self.assertEqual(o,before)

    def test_english_ui_is_supported_without_translating_payload(self):
        d,o=pair('dev-pf-audit');d['language']='English'
        text=render_output(d,o)
        self.assertIn('## Decision map',text)
        self.assertIn(o['result']['main_barrier'],text)
        self.assertIn(NOTICE,text)
