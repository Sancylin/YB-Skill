#!/usr/bin/env python3
"""Convert a schemaVersion=2 run in a separate directory; evidence must be recaptured and validated."""
import argparse
import json
import shutil
from pathlib import Path


def migrate(source, destination):
    source=Path(source).resolve(); destination=Path(destination).resolve()
    run=json.loads(source.read_text())
    if run.get('schemaVersion')!=2: raise ValueError('Only schemaVersion=2 runs can be converted')
    if destination.exists() or destination.is_relative_to(source.parent):
        raise ValueError('Destination must be new and outside the source run')
    if any(p.is_symlink() for p in source.parent.rglob('*')):
        raise ValueError('Resolve source symlinks before migration')
    shutil.copytree(source.parent,destination)
    run.update(schemaVersion=3,status='paused-blocked',nextAction='resume-plan')
    run['migration']={'fromVersion':2,'status':'needs-recapture','sourceRun':str(source),
        'required':['original inputs','exact fill targets','complete catalog classification','computed comparisons','current independent reviews']}
    run['blockers']=[{'id':'v3-recapture','reason':'Conversion is structural only; recapture and validate evidence against the run schema.'}]
    (destination/'run.v2.json').write_text(source.read_text())
    (destination/'run.json').write_text(json.dumps(run,ensure_ascii=False,indent=2))
    return destination/'run.json'

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source');p.add_argument('destination');a=p.parse_args()
    try: print(migrate(a.source,a.destination))
    except (ValueError,OSError) as e: p.exit(1,str(e)+'\n')
