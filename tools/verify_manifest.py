#!/usr/bin/env python3
"""Check every listed release file against SHA-256. No external dependencies."""
from pathlib import Path
import argparse,hashlib,json,sys

def verify(root):
    root=Path(root).resolve();m=json.loads((root/'MANIFEST.json').read_text());errors=[];seen=set()
    for row in m['files']:
        name=row['path'];p=root/name
        if name in seen:errors.append('Duplicate manifest path: '+name)
        seen.add(name)
        if p.is_symlink() or not p.resolve().is_relative_to(root):errors.append('Unsafe path: '+name);continue
        if not p.is_file():errors.append('Missing: '+name);continue
        b=p.read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:errors.append('Hash or size mismatch: '+name)
    return {'status':'PASS' if not errors else 'FAIL','listed_files':len(m['files']),'errors':errors,
            'scope':'Listed-file integrity only; not an independent signed provenance attestation.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',default=str(Path(__file__).resolve().parents[1]));a=p.parse_args()
    try:r=verify(a.root);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='PASS' else 1)
    except (OSError,ValueError,KeyError) as e:print(str(e),file=sys.stderr);raise SystemExit(2)
