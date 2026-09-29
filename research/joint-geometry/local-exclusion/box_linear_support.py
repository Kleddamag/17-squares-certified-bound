from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import json,sys,datetime,numpy as np
from scipy.optimize import linprog
R=Path(__file__).resolve().parent;OLD=R.parent/'round-23-proof-loop-01';A=F(461300,467001);L=F(4613,1000);zero=F(0);one=F(1)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[1],-a[0])
def sub(a,b):return add(a,neg(b))
def mul(a,b):v=[x*y for x in a for y in b];return min(v),max(v)
def ab(a):return (max(zero,a[0],-a[1]),max(abs(a[0]),abs(a[1])))
def si(t):return 2*t/(1+t*t)
def co(t):return (1-t*t)/(1+t*t)
def tr(a,b):return (min(co(a),co(b)),max(co(a),co(b),one if a<=0<=b else zero)),(si(a),si(b))
def dot(a,b):return add(mul(a[0],b[0]),mul(a[1],b[1]))
def axis(t):return [(co(t),si(t)),(-si(t),co(t))]
def js(v):
 if isinstance(v,F):return str(v)
 if isinstance(v,(tuple,list)):return[js(z) for z in v]
 if isinstance(v,dict):return{k:js(z) for k,z in v.items()}
 return v
input_path=Path(sys.argv[1]);tag=sys.argv[2];source=json.loads(input_path.read_text());boxes=[[F(z) for z in b] for b in source['boxes']];axes=[];mids=[];eps=None;eta=None
for b in boxes:
 ta,tb=b[4:];cs,ss=tr(ta,tb);axes.append([(cs,ss),(neg(ss),cs)]);mids.append(axis((ta+tb)/2))
rows=[];receipts=[];bounds=[(b[k],b[k+1]) for b in boxes for k in [0,2]]
for i,j in combinations(range(17),2):
 d=[(boxes[j][k]-boxes[i][k+1],boxes[j][k+1]-boxes[i][k]) for k in [0,2]];allowed=[];case_info=[]
 for owner in [i,j]:
  other=j if owner==i else i
  for k in range(2):
   ax=axes[owner][k];r=A*(one+ab(dot(ax,axes[other][0]))[0]+ab(dot(ax,axes[other][1]))[0])/2
   for sign in [-1,1]:
    n=[mul((F(sign),F(sign)),z) for z in ax];p=dot(n,d);ok=p[1]>=r;case_info.append(dict(owner=owner,k=k,sign=sign,projection=list(p),radius_lower=r,allowed=ok))
    if ok:allowed.append((owner,k,sign,n,r))
 if not allowed:
  receipts.append(dict(i=i,j=j,cases=case_info,immediate_incompatible=True));continue
 # Generate one valid necessary halfspace per distinct surviving midpoint normal.
 normals=sorted(set(tuple(sign*z for z in mids[owner][k]) for owner,k,sign,n,r in allowed))
 for nx,ny in normals:
  vals=[]
  for owner,k,sign,n,r in allowed:
   correction=dot([sub((nx,nx),n[0]),sub((ny,ny),n[1])],d)[0];vals.append(r+correction)
  lower=min(vals);a=[zero]*34;a[2*i]=nx;a[2*i+1]=ny;a[2*j]=-nx;a[2*j+1]=-ny;rows.append((a,-lower));receipts.append(dict(i=i,j=j,cases=case_info,normal=[nx,ny],lower=lower,row_index=len(rows)-1))
arr=np.array([[float(v) for v in a]+[-1.] for a,b in rows]);bb=np.array([float(b) for a,b in rows]);eligible={5,6,9,11,13};subids=[i for i,(a,b) in enumerate(rows) if all(k//2 in eligible for k,z in enumerate(a) if z)];rr=linprog(np.r_[np.zeros(34),1.],A_ub=arr[subids],b_ub=bb[subids],bounds=[tuple(map(float,b)) for b in bounds]+[(None,None)],method='highs');out=dict(status='NUMERICAL_PHASE_I_ONLY',target=str(L/A),epsilon=eps,t_radius=eta,boxes=boxes,midpoint_axes=mids,rows=[dict(a=a,b=b) for a,b in rows],pair_derivations=receipts,solver_status=int(rr.status),solver_message=rr.message,phase_I=None if rr.fun is None else float(rr.fun),utc=datetime.datetime.now(datetime.timezone.utc).isoformat());
if rr.success:
 scale=10**12;lam=[F(0)]*len(rows)
 for idx,v in zip(subids,rr.ineqlin.marginals):lam[idx]=F(max(0,round(-v*scale)),scale)
 residual=[sum(w*a[k] for w,(a,b) in zip(lam,rows)) for k in range(34)];rhs=sum(w*b for w,(a,b) in zip(lam,rows));lhs=sum(v*(lo if v>=0 else hi) for v,(lo,hi) in zip(residual,bounds));margin=lhs-rhs;out.update(source_boxes=str(input_path),multipliers=lam,residual=residual,rhs=rhs,residual_box_minimum=lhs,exact_exclusion_surplus=margin,exact_linear_infeasible=margin>0,active_dual_rows=sum(w>0 for w in lam),numerical_centers=None if rr.x is None else rr.x[:34].tolist())
if rr.success and rr.fun<0:
 centers=[min(max(F(float(v)).limit_denominator(10**10),lo),hi) for v,(lo,hi) in zip(rr.x[:34],bounds)];slacks=[b-sum(a[k]*centers[k] for k in range(34)) for a,b in rows];inside=all(lo<=v<=hi for v,(lo,hi) in zip(centers,bounds));out.update(rational_centers=centers,linear_witness_valid=inside and min(slacks)>=0,minimum_linear_slack=min(slacks))
(R/'outputs'/f'{tag}.json').write_text(json.dumps(js(out),indent=2));print(json.dumps({k:js(v) for k,v in out.items() if k in ['status','phase_I','exact_exclusion_surplus','exact_linear_infeasible','active_dual_rows','solver_message']}),flush=True)
