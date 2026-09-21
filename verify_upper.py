"""Exact verifier for a 17-unit-square packing. Python 3; no dependencies.

Run: python3 verify-packing.py [upper-packing-certificate.json]
Only rational arithmetic is used in every pass/fail decision.
"""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import json,sys

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def verify(path):
    data=json.loads(Path(path).read_text());L=F(data['side'])
    assert L>0
    squares=[];wall_slacks=[];pair_slacks=[]
    assert len(data['squares'])==17
    for entry in data['squares']:
        x,y,t=(F(entry[k]) for k in ('x','y','t'))
        u=((1-t*t)/(1+t*t),2*t/(1+t*t));v=(-u[1],u[0])
        assert dot(u,u)==1 and dot(v,v)==1 and dot(u,v)==0
        points=[(x+(a*u[0]+b*v[0])/2,y+(a*u[1]+b*v[1])/2) for a,b in product((-1,1),repeat=2)]
        for px,py in points:
            assert 0<=px<=L and 0<=py<=L,'Outside container'
            wall_slacks.extend((px,L-px,py,L-py))
        squares.append((u,v,points))
    for (i,A),(j,B) in combinations(enumerate(squares),2):
        gaps=[]
        for axis in (A[0],A[1],B[0],B[1]):
            p=[dot(axis,v) for v in A[2]];q=[dot(axis,v) for v in B[2]]
            gaps.extend((min(q)-max(p),min(p)-max(q)))
        gap=max(gaps)
        assert gap>=0,f'Squares {i+1} and {j+1} overlap'
        pair_slacks.append(gap)
    print('PASS: 17 exact unit squares; 68 vertices contained; all 136 pairs separated.')
    print('Exact container side:',L)
    # These decimal diagnostics do not participate in the proof decisions.
    print('Smallest wall clearance (decimal display only):',float(min(wall_slacks)))
    print('Smallest pair separation (decimal display only):',float(min(pair_slacks)))
    return {'unit_squares':17,'vertices':68,'pairs':136,'side':str(L),
            'wall_clearance_positive':min(wall_slacks)>0,
            'pair_clearance_positive':min(pair_slacks)>0}

if __name__=='__main__':
    verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name('upper-packing-certificate.json'))
