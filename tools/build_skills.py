#!/usr/bin/env python3
"""Generate self-contained skills from one canonical specification. Never installs them."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]

def products():
    idx=json.loads((ROOT/'protocols/index.json').read_text())
    common=(ROOT/'protocols/common.md').read_text()
    for p in idx['protocols']:
        pid=p['id']; name=p['name']; purpose=p['purpose']
        description=f'Use only when the user explicitly requests {name}. {purpose} Do not automatically combine this with other modes.'
        content='---\nname: '+pid+'\ndescription: '+json.dumps(description,ensure_ascii=False)+'\nmetadata:\n  author: "Eugene Prudchenko"\n  version: "'+idx['version']+'"\n---\n\n'
        content+='# '+name+'\n\n'+common+'\n'+(ROOT/p['source']).read_text()+'\n'
        content+='## Optional machine-mode references\nWhen explicitly asked for machine-mode JSON, use [input contract](references/input.schema.json) and [output contract](references/output.schema.json). For ordinary chat, use the readable output described above.\n'
        yield f'skills/{pid}/SKILL.md',content
        yield f'skills/{pid}/agents/openai.yaml',f'interface:\n  display_name: "{name}"\n  short_description: '+json.dumps(purpose)+'\n  default_prompt: "Use $'+pid+' on the material I provide, within its stated evidence and ethical boundaries."\npolicy:\n  allow_implicit_invocation: false\n'
        yield f'skills/{pid}/references/input.schema.json',(ROOT/'schemas/input.schema.json').read_text()
        yield f'skills/{pid}/references/output.schema.json',(ROOT/f'schemas/{pid}.output.schema.json').read_text()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');a=parser.parse_args()
    mismatches=[]
    for name,content in products():
        path=ROOT/name
        if a.check:
            if not path.exists() or path.read_text()!=content:mismatches.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
    if mismatches:print('Generated skill drift: '+', '.join(mismatches),file=sys.stderr);return 1
    print('PASS: five self-contained skills match canonical protocol sources.' if a.check else 'Built five self-contained skills.')
    return 0
if __name__=='__main__':raise SystemExit(main())
