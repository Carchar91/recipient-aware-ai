from __future__ import annotations
import contextlib,io,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from rai.core import ROOT,ContractError,digest,load_json
from tools import blind_review,live_eval


class EvaluationTests(unittest.TestCase):
    def test_nonobject_model_outputs_remain_recorded_failures(self):
        for output in (None,[],"not an object",7):
            with self.subTest(output=output),tempfile.TemporaryDirectory() as directory:
                def fake_call(data,model,**kwargs):
                    return {'origin':'live_provider_response','case_id':data['case_id'],
                      'arm':kwargs['arm'],'input_sha256':digest(data),'status':'contract_fail',
                      'output':output,'contract_errors':['$: expected object'],
                      'semantic_verdict':'not_reviewed'}
                argv=['live_eval.py','--model','mock-model','--case','rv-01','--execute',
                  '--allow-network','--acknowledge-cost','--max-calls','2','--out',directory]
                with patch.object(sys,'argv',argv),patch.dict(os.environ,{'OPENAI_API_KEY':'not-a-real-key'}),\
                     patch.object(live_eval,'call_model',side_effect=fake_call) as caller,\
                     patch('urllib.request.urlopen') as network,\
                     contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(live_eval.main(),1)
                self.assertEqual(caller.call_count,2)
                network.assert_not_called()
                run=next(Path(directory).glob('run-*'))
                summary=load_json(run/'summary.json')
                records=[load_json(path) for path in run.glob('*.json') if path.name not in ('plan.json','summary.json')]
                self.assertEqual(len(records),2)
                self.assertEqual(summary['samples'],2)
                self.assertEqual(summary['contract_pass'],0)
                self.assertEqual(summary['errors_or_contract_failures'],2)
                self.assertEqual(summary['semantic_verdict'],'not_reviewed')
                for record in records:
                    self.assertEqual(record['output'],output)
                    self.assertEqual(record['status'],'contract_fail')
                    self.assertFalse(record['expected_decision_match'])

    def test_blinded_review_rejects_changed_input_before_writing_pack(self):
        case=load_json(ROOT/'evals/cases/rv-01.json')
        changed_input=dict(case['input'],goal='Changed after the model run')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);run=root/'run';run.mkdir();out=root/'review'
            record={'origin':'live_provider_response','case_id':'rv-01','arm':'protocol',
              'repeat':0,'input_sha256':digest(changed_input),'output':{}}
            (run/'response.json').write_text(json.dumps(record),encoding='utf-8')
            argv=['blind_review.py','--run-dir',str(run),'--out',str(out)]
            with patch.object(sys,'argv',argv),self.assertRaisesRegex(ContractError,'input has changed'):
                blind_review.main()
            self.assertFalse(out.exists())

    def test_blinded_review_accepts_matching_input_and_hides_arm(self):
        case=load_json(ROOT/'evals/cases/rv-01.json')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);run=root/'run';run.mkdir();out=root/'review'
            record={'origin':'live_provider_response','case_id':'rv-01','arm':'protocol',
              'repeat':0,'input_sha256':digest(case['input']),'output':{'fixture':'mock response'}}
            (run/'response.json').write_text(json.dumps(record),encoding='utf-8')
            argv=['blind_review.py','--run-dir',str(run),'--out',str(out)]
            with patch.object(sys,'argv',argv),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(blind_review.main(),0)
            sample=load_json(out/'R001.json')
            self.assertEqual(sample['input'],case['input'])
            self.assertEqual(sample['response'],record['output'])
            self.assertNotIn('arm',sample)
            self.assertEqual(load_json(out/'DO_NOT_GIVE_TO_REVIEWER.key.json')['R001']['arm'],'protocol')
