#!/usr/bin/env python3
"""Create deterministic experimental prerelease archives and integrity manifests."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','.venv','__pycache__','dist','runs','review-packs','.pytest_cache'}

def source_files(root=ROOT):
    result=[]
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if any(x in EXCLUDED or x.endswith('.egg-info') for x in rel.parts):continue
        if p.is_symlink():raise ValueError(f'Symlinks are not allowed in release sources: {rel}')
        if not p.is_file():continue
        if p.name=='MANIFEST.json' or p.suffix in ('.pyc','.pyo') or p.name=='.DS_Store':continue
        if p.name.startswith('.env'):raise ValueError('Environment files may not enter the release archive.')
        result.append(p)
    return result

def archive(path,entries):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,blob in sorted(entries):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,blob,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:raise ValueError('ZIP verification failed.')

def main():
    version=(ROOT/'VERSION').read_text().strip()
    files=source_files()
    manifest={'project':'recipient-aware-ai','version':version,
      'status':'experimental_prerelease','remote_publication':'not_performed_by_packaging',
      'license':'Apache-2.0','license_scope':'author_owned_materials; third-party terms retained','manifest_excludes_itself':True,
      'files':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'bytes':p.stat().st_size,
                'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    source_zip=dist/f'recipient-aware-ai-{version}.zip'
    archive(source_zip,[(f'recipient-aware-ai/{p.relative_to(ROOT).as_posix()}',p.read_bytes()) for p in files]+[('recipient-aware-ai/MANIFEST.json',(ROOT/'MANIFEST.json').read_bytes())])
    skill_files=[p for p in files if p.relative_to(ROOT).parts[0]=='skills']
    skill_notices={name:(ROOT/name).read_bytes() for name in ('LICENSE','NOTICE','THIRD_PARTY_NOTICES.md','LICENSE_PENDING.md')}
    skill_notices['INSTALLATION.md']=(ROOT/'docs/INSTALLATION.md').read_bytes()
    skill_manifest={'version':version,'license':'Apache-2.0','status':'experimental_prerelease',
     'license_scope':'author_owned_materials; third-party terms retained',
     'files':[{'path':p.relative_to(ROOT/'skills').as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in skill_files]}
    skill_manifest['files'] += [{'path':name,'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest()} for name,blob in sorted(skill_notices.items())]
    skill_zip=dist/f'recipient-aware-ai-skills-{version}.zip'
    archive(skill_zip,[(p.relative_to(ROOT/'skills').as_posix(),p.read_bytes()) for p in skill_files]+list(skill_notices.items())+[
      ('MANIFEST.json',(json.dumps(skill_manifest,indent=2)+'\n').encode())])
    checks=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in (source_zip,skill_zip))
    (dist/'SHA256SUMS.txt').write_text(checks)
    print(json.dumps({'files':len(files),'source_archive':str(source_zip),'skills_archive':str(skill_zip),'sha256sums':checks},indent=2))
if __name__=='__main__':main()
