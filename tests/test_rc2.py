"""Offline contract regressions; authored examples are NOT live skill responses."""
import copy, hashlib, json, unittest
from rai.core import ROOT, NOTICE, PROTOCOLS, compile_case, load_json, render_output, schema, validate_input, validate_output
from rai.provider import make_payload


def pair(cid):
    folder=ROOT/'development/rc2'/cid
    return load_json(folder/'input.json'),load_json(folder/'authored-output.json')

class RC2Tests(unittest.TestCase):
    def test_archived_contracts_cases_examples_and_article_unchanged(self):
        for name,digest in load_json(ROOT/'reports/RC1_PRESERVED_HASHES.json').items():
            with self.subTest(name=name):
                self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)

    def test_version_downgrade_cannot_silently_validate(self):
        d,o=pair('dev-pf-audit');o['schema_version']='1.0'
        self.assertTrue(validate_output(d,o))

    def test_unknown_version_rejected(self):
        d,_=pair('dev-pf-audit');d['schema_version']='2.0'
        self.assertTrue(validate_input(d))

    def test_unknown_perspective_id_rejected(self):
        d,_=pair('dev-pf-audit');d['perspective']['recipient_criteria']=['E999']
        self.assertTrue(validate_input(d))

    def test_known_and_private_cannot_overlap(self):
        d,_=pair('dev-rv-sequence');d['perspective']['recipient_known_evidence'].append('E6')
        self.assertTrue(validate_input(d))

    def test_material_condition_cannot_be_private(self):
        d,_=pair('dev-rv-sequence');d['perspective']['sender_private_evidence'].append('E4')
        self.assertTrue(validate_input(d))

    def test_agent_send_authority_is_not_supported(self):
        d,_=pair('dev-rl-ready');d['perspective']['agent_authority']='send'
        self.assertTrue(validate_input(d))

    def test_ledger_keeps_full_attribution(self):
        d,o=pair('dev-pf-sparse');d['material_conditions']=['E1']
        o['preserved_conditions']=[dict(evidence_id='E1',statement='Без договора не проведём')]
        self.assertTrue(validate_output(d,o))
        o['preserved_conditions'][0]['statement']=d['evidence'][0]['text']
        self.assertEqual(validate_output(d,o),[])

    def test_no_unsolicited_ledger_item(self):
        d,o=pair('dev-pf-sparse');o['preserved_conditions']=[dict(evidence_id='E1',statement=d['evidence'][0]['text'])]
        self.assertTrue(validate_output(d,o))

    def test_decision_map_requires_existing_evidence(self):
        d,o=pair('dev-pf-audit');o['result']['decision_map'][0]['evidence_refs']=['E999']
        self.assertTrue(validate_output(d,o))

    def test_semantic_payoff_summary_is_not_a_literal_gate_in_11(self):
        d,o=pair('dev-dh-sequence')
        self.assertNotIn(o['result']['payoff'],o['result']['body'])
        self.assertEqual(validate_output(d,o),[])

    def test_legacy_payoff_gate_retained(self):
        d=load_json(ROOT/'examples/dopamine-hooks/input.json');o=load_json(ROOT/'examples/dopamine-hooks/reference-output.json')
        o['result']['payoff']='A missing literal excerpt'
        self.assertTrue(validate_output(d,o))

    def test_reverse_cannot_claim_uninserted_answer(self):
        d,o=pair('dev-rv-sequence');o['result']['findings'][0]['inserted_answer']='Invented insertion'
        self.assertTrue(validate_output(d,o))

    def test_reverse_answer_cannot_use_declared_private_evidence(self):
        d,o=pair('dev-rv-sequence')
        o['result']['findings'][0]['answer_evidence_refs']=['E6']
        self.assertTrue(validate_output(d,o))

    def test_reverse_cannot_answer_without_evidence(self):
        d,o=pair('dev-rv-sequence');o['result']['findings'][0]['answer_evidence_refs']=[]
        self.assertTrue(validate_output(d,o))

    def test_reverse_cannot_leave_supported_answer_only_in_review(self):
        d,o=pair('dev-rv-sequence');o['result']['findings'][0]['inserted_answer']=''
        self.assertTrue(validate_output(d,o))

    def test_reverse_unknown_answer_remains_explicit(self):
        d,o=pair('dev-rv-sequence');f=o['result']['findings'][-1]
        self.assertEqual(f['inserted_answer'],'');self.assertEqual(f['answer_evidence_refs'],[])
        self.assertEqual(validate_output(d,o),[])
        self.assertNotIn('80 000',o['result']['revised_message'])

    def test_rail_relevant_branches_need_not_be_four(self):
        d,o=pair('dev-rl-ready');self.assertEqual(len(o['result']['branches']),2)
        self.assertEqual(validate_output(d,o),[])

    def test_rail_artifact_refs_checked(self):
        d,o=pair('dev-rl-ready');o['result']['artifacts'][0]['evidence_refs']=['E999']
        self.assertTrue(validate_output(d,o))

    def test_rail_blocker_step_must_exist(self):
        d,o=pair('dev-rl-gap');o['result']['blockers'][0]['blocked_step']='S999'
        self.assertTrue(validate_output(d,o))

    def test_rail_missing_artifact_contract_not_silently_legacy(self):
        d,o=pair('dev-rl-ready');del o['result']['artifacts']
        self.assertTrue(validate_output(d,o))

    def test_provider_schema_tracks_input_version_without_network(self):
        for version in ('1.0','1.1'):
            d=(load_json(ROOT/'examples/profiler/input.json') if version=='1.0' else pair('dev-pf-audit')[0])
            compiled=compile_case(d);payload=make_payload(compiled,'mock-model')
            self.assertEqual(compiled['schema_version'],version)
            self.assertEqual(payload['text']['format']['schema']['properties']['schema_version']['enum'],[version])

    def test_baseline_omits_index_purpose_and_selected_procedure(self):
        index=load_json(ROOT/'protocols/index.json')
        for row in index['protocols']:
            cid=next(x['case_id'] for x in load_json(ROOT/'development/rc2/cases.json') if x['protocol']==row['id'])
            d,_=pair(cid);compiled=compile_case(d,'baseline')
            self.assertNotIn(row['purpose'],compiled['system'])
            self.assertNotIn((ROOT/row['source']).read_text(),compiled['system'])
            self.assertIn('Machine response contract',compiled['system']) # still a component comparison

    def test_hooks_render_does_not_duplicate_opening_or_debug_summary(self):
        d,o=pair('dev-dh-sequence');text=render_output(d,o)
        self.assertEqual(text.count(o['result']['opening']),1)
        self.assertNotIn(o['result']['payoff'],text)
        self.assertIn(o['result']['payoff'],render_output(d,o,audit=True))

    def test_reverse_deliverable_precedes_operator_map(self):
        d,o=pair('dev-rv-sequence');text=render_output(d,o)
        self.assertLess(text.index(o['result']['revised_message']),text.index('Карта изменений — только оператору'))

    def test_rail_renderer_includes_prepared_artifacts_and_blockers(self):
        for cid in ('dev-rl-ready','dev-rl-gap'):
            d,o=pair(cid);text=render_output(d,o)
            for a in o['result']['artifacts']:self.assertIn(a['content'],text)
            for b in o['result']['blockers']:self.assertIn(b['missing'],text)

    def test_author_reverse_rating_is_absent_not_tie(self):
        review=load_json(ROOT/'reports/author_product_review.json')
        reverse=next(x for x in review['ratings'] if x['pair_id']=='P07')
        self.assertIsNone(reverse['selection']);self.assertIsNone(reverse['arm'])
        self.assertFalse(review['blind']);self.assertFalse(review['independent'])

for c in load_json(ROOT/'development/rc2/cases.json'):
    def check(self,c=c):
        d,o=pair(c['case_id'])
        self.assertEqual(validate_output(d,o),[])
        self.assertIn(NOTICE,render_output(d,o));self.assertFalse(c['held_out'])
    setattr(RC2Tests,'test_development_'+c['case_id'].replace('-','_'),check)
