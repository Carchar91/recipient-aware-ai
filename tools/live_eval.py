#!/usr/bin/env python3
"""Plan or execute a paired baseline/protocol evaluation. Human grading is separate."""
from __future__ import annotations
import argparse,json,random,sys,secrets
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from rai.core import load_json, digest, compile_case, ContractError
from rai.provider import call_model

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--model',required=True)
    p.add_argument('--case',action='append',dest='case_ids')
    p.add_argument('--repeats',type=int,default=1)
    p.add_argument('--max-calls',type=int,default=2)
    p.add_argument('--max-output-tokens',type=int,default=4096)
    p.add_argument('--execute',action='store_true')
    p.add_argument('--allow-network',action='store_true');p.add_argument('--acknowledge-cost',action='store_true')
    p.add_argument('--out',default='runs');p.add_argument('--seed',type=int,default=73)
    a=p.parse_args()
    if not 1<=a.repeats<=10 or not 1<=a.max_calls<=600:raise ContractError('Invalid repeat count or call cap.')
    paths=sorted((ROOT/'evals/cases').glob('*.json'))
    cases=[load_json(x) for x in paths]
    if a.case_ids:
        unknown=set(a.case_ids)-{x['id'] for x in cases}
        if unknown:raise ContractError('Unknown case IDs.')
        cases=[x for x in cases if x['id'] in a.case_ids]
    tasks=[(c,r,arm) for c in cases for r in range(a.repeats) for arm in ('baseline','protocol')]
    random.Random(a.seed).shuffle(tasks)
    plan={'mode':'execution' if a.execute else 'plan_only','model':a.model,'calls':len(tasks),
          'case_ids':[c['id'] for c in cases],'repeats':a.repeats,'max_output_tokens':a.max_output_tokens,
          'suite_sha256':digest(cases),'order_seed':a.seed,
          'comparison':'Same input, output schema and common safety rules. Detailed mode procedure only in protocol arm.',
          'limits':'Call count and output-token cap are not a money budget. Generation is not guaranteed deterministic.'}
    if not a.execute:
        print(json.dumps(plan,indent=2));return 0
    if len(tasks)>a.max_calls:raise ContractError(f'Plan requires {len(tasks)} calls, exceeds explicit cap {a.max_calls}.')
    if not (a.allow_network and a.acknowledge_cost):raise ContractError('Both network and paid-cost acknowledgment flags are required.')
    # Validate all inputs and credentials before the first chargeable request.
    import os
    if not os.environ.get('OPENAI_API_KEY'):raise ContractError('OPENAI_API_KEY missing; no request sent.')
    for c in cases:
        compile_case(c['input'])
        if not c['input']['privacy_ok']:raise ContractError('A case is not cleared for model transmission.')
    out=Path(a.out)/('run-'+secrets.token_hex(6));out.mkdir(parents=True,mode=0o700)
    (out/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    statuses=[]
    for index,(c,repeat,arm) in enumerate(tasks):
        record=call_model(c['input'],a.model,arm=arm,allow_network=True,acknowledge_cost=True,
                          max_output_tokens=a.max_output_tokens)
        # Expectations applied after generation, never included in model input.
        output=record.get('output')
        decision=output.get('decision') if isinstance(output,dict) else None
        record.update(repeat=repeat,suite_sha256=plan['suite_sha256'],
          expected_decision_match=decision in c['expected_decisions'])
        path=out/f'{index:03d}-{c["id"]}-{arm}-{repeat}.json'
        path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');path.chmod(0o600)
        statuses.append(record['status'])
        print(f'{c["id"]} {arm}: {record["status"]}',file=sys.stderr)
    summary={'samples':len(statuses),'contract_pass':statuses.count('contract_pass'),
             'errors_or_contract_failures':len(statuses)-statuses.count('contract_pass'),
             'semantic_verdict':'not_reviewed','not_an_efficacy_score':True}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(str(out));return 0 if all(x=='contract_pass' for x in statuses) else 1
if __name__=='__main__':
    try:raise SystemExit(main())
    except (ContractError,OSError,ValueError) as e:print(str(e),file=sys.stderr);raise SystemExit(2)
