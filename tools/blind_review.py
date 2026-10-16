#!/usr/bin/env python3
"""Hide arm labels from a reviewer; keep answer content and evaluation inputs visible."""
import argparse,json,sys,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from rai.core import load_json, digest, ContractError

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-dir',required=True);p.add_argument('--out',required=True);p.add_argument('--seed',type=int,default=101);a=p.parse_args()
    run=Path(a.run_dir);out=Path(a.out)
    records=[load_json(x) for x in sorted(run.glob('*.json')) if x.name not in ('plan.json','summary.json')]
    records=[r for r in records if r.get('origin')=='live_provider_response']
    if not records:raise ContractError('No live response records. Do not present reference fixtures as live evaluation.')
    cases={}
    for r in records:
        case=load_json(ROOT/'evals/cases'/f'{r["case_id"]}.json')
        if digest(case['input'])!=r.get('input_sha256'):
            raise ContractError('Evaluation input has changed or its recorded hash is missing; restore the original case before blinded review.')
        cases[r['case_id']]=case
    out.mkdir(parents=True,exist_ok=False,mode=0o700)
    random.Random(a.seed).shuffle(records);key={};ratings=[]
    for i,r in enumerate(records):
        label=f'R{i+1:03d}';key[label]={'case_id':r['case_id'],'arm':r['arm'],'repeat':r['repeat']}
        case=cases[r['case_id']]
        review={'blind_id':label,'input':case['input'],'response':r.get('output',r.get('output_text','[No usable response]')),
                'human_checks':case['human_checks']}
        (out/f'{label}.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
        ratings.append({'blind_id':label,'reviewer':'','critical_failure':None,'factual_grounding':None,
          'uncertainty_discipline':None,'task_and_authority':None,'clarity_and_completion':None,
          'agency_and_good_faith':None,'evidence_quotes':[],'notes':''})
    (out/'ratings.template.json').write_text(json.dumps(ratings,indent=2)+'\n')
    key_path=out/'DO_NOT_GIVE_TO_REVIEWER.key.json';key_path.write_text(json.dumps(key,indent=2)+'\n');key_path.chmod(0o600)
    (out/'README.txt').write_text('Give the reviewer only R*.json and ratings.template.json, plus EVALUATION.md. Do not include the key. Blinding hides labels, not stylistic clues. Never score missing reviews as passes.\n')
    print(out);return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (ContractError,OSError,ValueError) as e:print(str(e),file=sys.stderr);raise SystemExit(2)
