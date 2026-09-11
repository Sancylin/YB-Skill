#!/usr/bin/env python3
"""Compute content differences or measured geometry. Inputs remain auditable."""
import argparse
import hashlib
import json
from pathlib import Path
from runlib.checks import content_diff,finite


def compare(data,kind):
    if kind=='content':
        media=data.get('media', ['figma','demo'])
        if not isinstance(media,list) or not media or any(x not in ('figma','demo') for x in media):raise ValueError('media must list actual deliverables')
        if not isinstance(data.get('source'),dict) or not data['source']:raise ValueError('Nonempty source content required')
        mismatches=[{'medium':medium,'path':path} for medium in media for path in content_diff(data.get('source'),data.get(medium))]
        return dict(data,mismatches=mismatches,verdict='fail' if mismatches else 'pass')
    rows=[]
    for e in data['elements']:
        fields=e.get('fields',list(e['live']))
        ds=[]
        for field in fields:
            a,b,t=e['live'].get(field),e['ours'].get(field),e['tolerances'].get(field)
            if not all(finite(v) for v in (a,b,t)) or t<0:raise ValueError('Finite geometry and nonnegative tolerance required')
            ds.append(dict(field=field,live=a,ours=b,delta=b-a,tolerance=t,status='within' if abs(b-a)<=t else 'open'))
        rows.append(dict(e,deltas=ds))
    return dict(data,elements=rows,verdict='pass' if rows and all(e['deltas'] and all(d['status']=='within' for d in e['deltas']) for e in rows) else 'fail')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('kind',choices=['content','baseline']);p.add_argument('input',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try:
        raw=a.input.read_bytes();result=compare(json.loads(raw),a.kind)
        result['computation']={'producer':'compare-evidence-v3','inputSha256':hashlib.sha256(raw).hexdigest()}
        with a.output.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    except (ValueError,KeyError,OSError,TypeError) as e:p.exit(1,str(e)+'\n')
