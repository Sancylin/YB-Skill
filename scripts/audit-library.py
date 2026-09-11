#!/usr/bin/env python3
"""Compare captured published catalog to local snapshot. No live API calls."""
import argparse
import hashlib
import json
from pathlib import Path


def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


FIELDS=('properties','dependencies','childInstanceTags')


def field_diff(a,b):
    return [f for f in FIELDS if a.get(f)!=b.get(f)]


def audit(local,live):
    a={x['nodeId']:x for x in local};b={x['nodeId']:x for x in live}
    if len(a)!=len(local) or len(b)!=len(live):raise ValueError('Duplicate node ids')
    rekeyed=[];changed=[]
    for node in sorted(a.keys() & b.keys()):
        old,new=a[node],b[node]
        if old.get('assetKey')!=new.get('assetKey'):
            rekeyed.append(dict(nodeId=node,name=new.get('name') or old.get('name'),
                                fromKey=old.get('assetKey'),toKey=new.get('assetKey'),fields=field_diff(old,new)))
            continue
        fields=field_diff(old,new)
        if fields:changed.append(dict(nodeId=node,assetKey=new.get('assetKey'),fields=fields))
    return dict(localCount=len(a),liveCount=len(b),
                added=sorted(b.keys()-a.keys()),removed=sorted(a.keys()-b.keys()),
                rekeyed=rekeyed,changed=changed,
                localFingerprint=fingerprint(local),liveFingerprint=fingerprint(live),visual='unknown',
                note='Keyed by nodeId; same-nodeId/different-assetKey is an identity migration, not a removal. '
                     'Matching schema is not proof of visual equivalence; validate each used asset.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('local',type=Path);p.add_argument('live',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try:
        result=audit(json.loads(a.local.read_text()),json.loads(a.live.read_text()))
        with a.output.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
        print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in result.items()},ensure_ascii=False))
    except (OSError,ValueError,KeyError) as e:p.exit(1,str(e)+'\n')
