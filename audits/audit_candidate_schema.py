"""Independent strict schema, D4 and integer budget audit for point/triple files."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys
from audit_controls import orbit,expand

p=Path(sys.argv[1]);raw=p.read_bytes();c=json.loads(raw)
L=F(c['L']);A=F(c['A']);D=c['coordinate_denominator']
assert L==F(4613,1000) and 0<A<L
assert type(D)is int and D>0 and (L*D).denominator==1
Z=int(L*D)
assert all(type(c[k])is int and c[k]>0 for k in ['weight_denominator','minimum_units','budget_units'])
assert 17*c['minimum_units']>c['budget_units']
assert F(c['bound'])==L/A
cursor=F(0)
for row in c['entries']:
 a,b,t,B=map(F,row)
 assert a==cursor and 0<=a<b<1 and 0<=t<1 and 0<B<A
 cursor=b
assert cursor*cursor+2*cursor>1
N=0
for x,y,w in c['point_orbits']:
 assert all(type(z)is int for z in (x,y,w))
 assert 0<=x<=Z and 0<=y<=Z and w>=0
 N+=len(orbit((x,y),Z))
for group in c['threshold_orbits']:
 assert type(group['weight'])is int and group['weight']>=0 and group['triples']
 for tri in group['triples']:
  assert len(tri)==len(set(tri))==3
  assert all(type(i)is int and 0<=i<N for i in tri)
sites,weights,triples,_=expand(c)
absolute=sum(weights)+5*sum(w for tri,w in triples)
assert absolute<2**50
out={'status':'PASS_INDEPENDENT_CANDIDATE_SCHEMA_D4_BUDGET',
 'certificate_sha256':hashlib.sha256(raw).hexdigest(),'A':str(A),'bound':str(L/A),
 'intervals':len(c['entries']),'sites':len(sites),'physical_triples':len(triples),
 'minimum_units':c['minimum_units'],'budget_units':c['budget_units'],
 'counting_surplus_units':17*c['minimum_units']-c['budget_units'],
 'absolute_signed_weight_units':absolute,
 'scope':'Structural and arithmetic premises; exact full geometry replays are separately required.'}
(Path(__file__).parent/'average4-global-schema-independent-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
