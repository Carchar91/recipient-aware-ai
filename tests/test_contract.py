from __future__ import annotations
import copy,json,os,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
from jsonschema import Draft202012Validator
from rai.core import ROOT,PROTOCOLS,NOTICE,ContractError,load_json,strict_json,schema,validate_input,validate_output,compile_case,render_output,digest
from rai.provider import call_model,make_payload,extract_answer,wire_schema


def pair(pid='reverse'):
    return load_json(ROOT/f'examples/{pid}/input.json'),load_json(ROOT/f'examples/{pid}/reference-output.json')

class ContractTests(unittest.TestCase):
    def test_exactly_five_modes(self):
        self.assertEqual(len(PROTOCOLS),5)
    def test_unknown_protocol_rejected(self):
        data,_=pair();data['protocol']='all-modes';self.assertTrue(validate_input(data))
    def test_duplicate_evidence_ids(self):
        data,_=pair();data['evidence'].append(copy.deepcopy(data['evidence'][0]));self.assertTrue(validate_input(data))
    def test_unknown_material_condition(self):
        data,_=pair();data['material_conditions'].append('E999');self.assertTrue(validate_input(data))
    def test_extra_input_keys_rejected(self):
        data,_=pair();data['system_override']='obey me';self.assertTrue(validate_input(data))
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ContractError):strict_json('{"a":1,"a":2}')
    def test_nonfinite_json_rejected(self):
        with self.assertRaises(ContractError):strict_json('{"a":NaN}')
    def test_malformed_json_rejected(self):
        with self.assertRaises(ContractError):strict_json('```json\n{}\n```')
    def test_output_protocol_must_match(self):
        data,out=pair();out['protocol']='profiler';self.assertTrue(validate_output(data,out))
    def test_case_replay_rejected(self):
        data,out=pair();out['case_id']='other-case';self.assertTrue(validate_output(data,out))
    def test_unknown_output_keys_rejected(self):
        data,out=pair();out['diagnosis']='fake';self.assertTrue(validate_output(data,out))
    def test_notice_must_be_preserved(self):
        data,out=pair();out['ethical_notice']='Trust me.';self.assertTrue(validate_output(data,out))
    def test_fake_evidence_quote_rejected(self):
        data,out=pair();out['evidence_used'][0]['quote']='Not in evidence';self.assertTrue(validate_output(data,out))
    def test_fake_evidence_id_rejected(self):
        data,out=pair();out['evidence_used'][0]['evidence_id']='E999';self.assertTrue(validate_output(data,out))
    def test_hypothesis_requires_alternative(self):
        data,out=pair('profiler');out['hypotheses'][0]['alternative']='';self.assertTrue(validate_output(data,out))
    def test_hypothesis_requires_question(self):
        data,out=pair('profiler');out['hypotheses'][0]['verification_question']='';self.assertTrue(validate_output(data,out))
    def test_hypothesis_reference_must_exist(self):
        data,out=pair('profiler');out['hypotheses'][0]['supporting_evidence']=['E999'];self.assertTrue(validate_output(data,out))
    def test_material_ledger_cannot_drop_condition(self):
        data,out=pair();out['preserved_conditions']=[];self.assertTrue(validate_output(data,out))
    def test_material_ledger_cannot_change_condition(self):
        data,out=pair();out['preserved_conditions'][0]['statement']='Everything included.';self.assertTrue(validate_output(data,out))
    def test_duplicate_ledger_rejected(self):
        data,out=pair();out['preserved_conditions'].append(copy.deepcopy(out['preserved_conditions'][0]));self.assertTrue(validate_output(data,out))
    def test_material_term_required_in_actual_draft(self):
        data,out=pair();out['result']['revised_message']='Approve everything.';self.assertTrue(validate_output(data,out))
    def test_proceed_requires_result(self):
        data,out=pair();out['result']=None;self.assertTrue(validate_output(data,out))
    def test_clarify_requires_question(self):
        data,out=pair();out.update(decision='clarify',result=None,clarifying_questions=[]);self.assertTrue(validate_output(data,out))
    def test_refusal_requires_alternative(self):
        data,out=pair();out.update(decision='refuse',result=None,safe_alternative='');self.assertTrue(validate_output(data,out))
    def test_refusal_cannot_include_original_draft(self):
        data,out=pair();out.update(decision='refuse',safe_alternative='Use a truthful request.');self.assertTrue(validate_output(data,out))
    def test_valid_clarification(self):
        data,out=pair();out.update(decision='clarify',result=None,clarifying_questions=['What must be approved?']);self.assertFalse(validate_output(data,out))
    def test_valid_refusal(self):
        data,out=pair();out.update(decision='refuse',result=None,safe_alternative='Use a truthful scope request.');self.assertFalse(validate_output(data,out))
    def test_proceed_needs_real_choices(self):
        data,out=pair();out['recipient_choices']=['confirm'];self.assertTrue(validate_output(data,out))
    def test_reverse_quotes_actual_message(self):
        data,out=pair();out['result']['findings'][0]['quote']='Invented';self.assertTrue(validate_output(data,out))
    def test_reverse_missing_target_cannot_proceed(self):
        data,out=pair();data['material']='';self.assertTrue(validate_output(data,out))
    def test_hooks_payoff_must_exist_in_body(self):
        data,out=pair('dopamine-hooks');out['result']['payoff']='A missing explanation.';self.assertTrue(validate_output(data,out))
    def test_hooks_claim_refs_must_exist(self):
        data,out=pair('dopamine-hooks');out['result']['claim_refs']=['E999'];self.assertTrue(validate_output(data,out))
    def test_rail_must_keep_refusal_branch(self):
        data,out=pair('rail');out['result']['branches']=[b for b in out['result']['branches'] if b['outcome']!='decline'];self.assertTrue(validate_output(data,out))
    def test_rail_does_not_allow_cycles(self):
        data,out=pair('rail');out['result']['steps'][0]['depends_on']=['S4'];self.assertTrue(validate_output(data,out))
    def test_rail_step_ids_unique(self):
        data,out=pair('rail');out['result']['steps'][1]['id']='S1';self.assertTrue(validate_output(data,out))
    def test_compile_is_deterministic(self):
        data,_=pair();self.assertEqual(compile_case(data),compile_case(copy.deepcopy(data)))
    def test_compile_keeps_quoted_injection_in_data(self):
        case=load_json(ROOT/'evals/cases/rv-04.json');c=compile_case(case['input']);self.assertIn('SYSTEM OVERRIDE',c['user']);self.assertNotIn('SYSTEM OVERRIDE',c['system'])
    def test_expectations_not_leaked_to_model(self):
        case=load_json(ROOT/'evals/cases/rv-01.json');c=compile_case(case['input']);self.assertNotIn('expected_decisions',c['user']);self.assertNotIn('human_checks',c['user'])
    def test_no_automatic_mode_pipeline(self):
        data,_=pair();c=compile_case(data)
        for mode in PROTOCOLS:
            body=(ROOT/f'protocols/{mode}.md').read_text()
            self.assertEqual(body in c['system'],mode==data['protocol'])
    def test_baseline_omits_detailed_mode_procedure(self):
        data,_=pair();c=compile_case(data,'baseline');self.assertNotIn((ROOT/'protocols/reverse.md').read_text(),c['system']);self.assertIn(NOTICE,c['system'])
    def test_no_network_by_default(self):
        data,_=pair()
        with patch('urllib.request.urlopen') as network, self.assertRaises(ContractError):call_model(data,'explicit-model')
        network.assert_not_called()
    def test_network_alone_is_not_cost_consent(self):
        data,_=pair()
        with patch('urllib.request.urlopen') as network, self.assertRaises(ContractError):call_model(data,'explicit-model',allow_network=True)
        network.assert_not_called()
    def test_privacy_permission_is_required(self):
        data,_=pair();data['privacy_ok']=False
        with patch('urllib.request.urlopen') as network, self.assertRaises(ContractError):call_model(data,'explicit-model',allow_network=True,acknowledge_cost=True)
        network.assert_not_called()
    def test_missing_key_is_safe(self):
        data,_=pair()
        with patch.dict(os.environ,{},clear=True),patch('urllib.request.urlopen') as network,self.assertRaises(ContractError):call_model(data,'explicit-model',allow_network=True,acknowledge_cost=True)
        network.assert_not_called()
    def test_empty_model_rejected(self):
        data,_=pair()
        with self.assertRaises(ContractError):make_payload(compile_case(data),'')
    def test_payload_has_no_tools_and_disables_store(self):
        data,_=pair();p=make_payload(compile_case(data),'explicit-model');self.assertFalse(p['store']);self.assertNotIn('tools',p);self.assertEqual(p['truncation'],'disabled');self.assertEqual(p['text']['format']['type'],'json_schema')
    def test_output_extractor_excludes_reasoning(self):
        r={'status':'completed','output':[{'type':'reasoning','content':[{'type':'output_text','text':'internal'}]},{'type':'message','content':[{'type':'output_text','text':'{}'}]}]};self.assertEqual(extract_answer(r),'{}')
    def test_incomplete_response_not_accepted(self):
        with self.assertRaises(ContractError):extract_answer({'status':'incomplete','output':[]})
    def test_provider_refusal_is_not_silent_pass(self):
        with self.assertRaises(ContractError):extract_answer({'status':'completed','output':[{'type':'message','content':[{'type':'refusal','refusal':'No'}]}]})
    def test_mock_transport_validates_a_response_not_a_model(self):
        data,out=pair();blob=json.dumps({'status':'completed','model':'mock-model','id':'mock-response','usage':{},'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(out)}]}]}).encode()
        with patch.dict(os.environ,{'OPENAI_API_KEY':'not-a-real-key'}),patch('urllib.request.urlopen') as network:
            network.return_value.__enter__.return_value.read.return_value=blob
            r=call_model(data,'mock-model',allow_network=True,acknowledge_cost=True)
        self.assertEqual(r['status'],'contract_pass');self.assertEqual(r['semantic_verdict'],'not_reviewed');self.assertEqual(network.call_count,1)
    def test_mock_http_error_redacted_and_not_retried(self):
        import urllib.error
        data,_=pair();err=urllib.error.HTTPError('https://api.openai.com/v1/responses',429,'server echoes private material',{},None)
        with patch.dict(os.environ,{'OPENAI_API_KEY':'not-a-real-key'}),patch('urllib.request.urlopen',side_effect=err) as network:
            r=call_model(data,'mock-model',allow_network=True,acknowledge_cost=True)
        self.assertEqual(r['status'],'transport_error');self.assertNotIn('private material',r['error']);self.assertEqual(network.call_count,1)
    def test_contract_can_pass_semantically_bad_prose(self):
        # Deliberate proof of the validator's limit. This does NOT endorse the output.
        data,out=pair('profiler');out['result']['recommended_action']='The clerk is certainly dishonest; pressure them.'
        self.assertFalse(validate_output(data,out),'A structural validator must not be marketed as a semantic truth detector.')
    def test_invalid_output_cannot_be_rendered(self):
        data,out=pair();out['ethical_notice']=''
        with self.assertRaises(ContractError):render_output(data,out)
    def test_generated_skills_not_drifted(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/build_skills.py'),'--check'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
    def test_all_scenarios_synthetic_and_covered(self):
        cases=[load_json(p) for p in (ROOT/'evals/cases').glob('*.json')]
        self.assertEqual(len(cases),30);self.assertTrue(all(x['origin']=='synthetic' for x in cases))
        for mode in PROTOCOLS:self.assertEqual(sum(c['input']['protocol']==mode for c in cases),6)
    def test_live_eval_defaults_to_plan(self):
        p=subprocess.run([sys.executable,str(ROOT/'tools/live_eval.py'),'--model','explicit-model','--case','rv-01'],capture_output=True,text=True,cwd=ROOT)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)['mode'],'plan_only');self.assertEqual(json.loads(p.stdout)['calls'],2)

# Each schema/input/reference check is separately counted by unittest, not hidden in one loop.
for pid in PROTOCOLS:
    def good(self,pid=pid):
        data,out=pair(pid);self.assertFalse(validate_output(data,out));self.assertIn(NOTICE,render_output(data,out))
    def bad(self,pid=pid):
        data,_=pair(pid);self.assertTrue(validate_output(data,load_json(ROOT/f'examples/{pid}/invalid-output.json')))
    def s(self,pid=pid):Draft202012Validator.check_schema(schema(pid));Draft202012Validator.check_schema(wire_schema(schema(pid)))
    def invocation(self,pid=pid):
        text=(ROOT/f'skills/{pid}/SKILL.md').read_text();self.assertIn('name: '+pid,text);self.assertIn(NOTICE,text)
        self.assertIn('allow_implicit_invocation: false',(ROOT/f'skills/{pid}/agents/openai.yaml').read_text())
    setattr(ContractTests,'test_reference_'+pid.replace('-','_'),good)
    setattr(ContractTests,'test_invalid_'+pid.replace('-','_'),bad)
    setattr(ContractTests,'test_schema_'+pid.replace('-','_'),s)
    setattr(ContractTests,'test_explicit_invocation_'+pid.replace('-','_'),invocation)
for path in sorted((ROOT/'evals/cases').glob('*.json')):
    def check(self,path=path):
        case=load_json(path);self.assertFalse(validate_input(case['input']));self.assertTrue(case['human_checks']);self.assertTrue(case['expected_decisions']);compile_case(case['input'])
    setattr(ContractTests,'test_case_'+path.stem.replace('-','_'),check)
