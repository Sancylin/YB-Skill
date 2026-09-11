import math
import unicodedata


def normalize(value):
    if isinstance(value, str):
        return unicodedata.normalize('NFC', value.replace('\r\n', '\n').replace('\r', '\n'))
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize(v) for v in value]
    return value


def content_diff(source, actual, path=''):
    if not isinstance(source, dict) or not isinstance(actual, dict):
        return [path or '/']
    out=[]
    for key in sorted(source.keys() | actual.keys()):
        p=path+'/'+key
        if key not in source or key not in actual:
            out.append(p)
        elif isinstance(source[key],dict) and isinstance(actual[key],dict):
            out.extend(content_diff(source[key],actual[key],p))
        elif normalize(source[key]) != normalize(actual[key]):
            out.append(p)
    return out


def finite(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)


def fill_errors(before, after, adjustments):
    """fills is {descendantId: [paint,...]}; exact paint visibility edits only."""
    if not isinstance(before,dict) or not isinstance(after,dict):
        return ['fills must map descendant node IDs to paint arrays']
    expected={}
    errors=[]
    for item in adjustments:
        node=item.get('nodeId'); index=item.get('paintIndex'); prop=item.get('property')
        if not isinstance(node,str) or type(index) is not int or index<0 or prop not in ('visible','opacity'):
            errors.append('invalid exact fill target'); continue
        key=(node,index,prop)
        if key in expected: errors.append('duplicate fill adjustment')
        expected[key]=item
    actual=set()
    if before.keys()!=after.keys(): errors.append('fill node set changed')
    for node in before.keys() & after.keys():
        a,b=before[node],after[node]
        if not isinstance(a,list) or not isinstance(b,list) or len(a)!=len(b):
            errors.append('paint array length/type changed');continue
        for i,(x,y) in enumerate(zip(a,b)):
            if not isinstance(x,dict) or not isinstance(y,dict):
                errors.append('paint must be an object');continue
            for prop in x.keys() | y.keys():
                if prop in x and prop in y and x[prop]==y[prop]:continue
                key=(node,i,prop);actual.add(key)
                item=expected.get(key)
                if not item or prop not in x or prop not in y:
                    errors.append('unauthorized fill difference');continue
                if item.get('before')!=x[prop] or item.get('after')!=y[prop]:
                    errors.append('fill adjustment values differ from capture')
                if prop=='visible' and not (x[prop] is True and y[prop] is False):
                    errors.append('only hiding visible paint is allowed')
                if prop=='opacity' and not (finite(x[prop]) and 0<x[prop]<=1 and type(y[prop]) in (int,float) and y[prop]==0):
                    errors.append('only setting paint opacity to zero is allowed')
    if actual!=set(expected): errors.append('fill adjustments do not exactly cover observed changes')
    return errors
