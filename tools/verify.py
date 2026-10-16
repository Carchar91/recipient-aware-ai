#!/usr/bin/env python3
"""Offline engineering verification. Never calls models or GitHub."""
import argparse,contextlib,io,json,platform,sys,unittest,subprocess
from pathlib import Path
from importlib.metadata import version
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))

def main():
 p=argparse.ArgumentParser();p.add_argument('--report',default='reports/LOCAL_VERIFICATION.json');a=p.parse_args()
 generated=subprocess.run([sys.executable,str(ROOT/'tools/build_skills.py'),'--check'],capture_output=True,text=True)
 if generated.returncode:print(generated.stderr,file=sys.stderr);return 1
 suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
 stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
 report={'status':'PASS' if result.wasSuccessful() else 'FAIL','test_layer':'offline_engineering_only',
  'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
  'python':platform.python_version(),'dependencies':{x:version(x) for x in ('jsonschema','attrs','jsonschema-specifications','referencing','rpds-py','typing_extensions')},
  'scenario_count':len(list((ROOT/'evals/cases').glob('*.json'))),'protocol_count':5,'reference_outputs':5,
  'reference_output_origin':'assistant_authored_synthetic_fixtures',
  'live_model_calls':0,'live_evaluation_status':'NOT_RUN','independent_semantic_review':'NOT_RUN',
  'github_publication':'NOT_PERFORMED','license':'PENDING_OWNER_DECISION',
  'limits':'Passing schema, provenance-reference and mock-transport tests does not establish model behavior, semantic truth, safety or efficacy.'}
 target=ROOT/a.report;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(report,indent=2)+'\n')
 target.with_suffix('.log').write_text(stream.getvalue())
 print(json.dumps(report,indent=2));return 0 if result.wasSuccessful() else 1
if __name__=='__main__':raise SystemExit(main())
