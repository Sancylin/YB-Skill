#!/usr/bin/env python3
"""Build a clean, complete, reproducible Skill ZIP from the maintained whitelist."""
import argparse
import importlib.util
import os
from pathlib import Path
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validate_skill',ROOT/'scripts/validate-skill.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def build(output):
    errors=module.validate(ROOT)
    if errors:
        raise ValueError('\n'.join(errors))
    files=module.managed_files(ROOT)
    if not (ROOT/'demo/package.json').is_file():
        raise ValueError('Complete package requires demo/package.json')
    output=output.resolve()
    output.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.skill-package-',suffix='.zip',dir=output.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(name,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                info=zipfile.ZipInfo(f'{ROOT.name}/{path.as_posix()}',date_time=(2020,1,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=(0o644 | 0o100000)<<16
                archive.writestr(info,(ROOT/path).read_bytes())
        with zipfile.ZipFile(name) as archive:
            if archive.testzip():
                raise ValueError('Archive integrity check failed')
            for path in files:
                if archive.read(f'{ROOT.name}/{path.as_posix()}')!=(ROOT/path).read_bytes():
                    raise ValueError(f'Archive differs from source: {path}')
        os.replace(name,output)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return len(files)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT.parent/f'{ROOT.name}.zip')
    args=parser.parse_args()
    print(f'OK: {build(args.output)} files -> {args.output.resolve()}')
