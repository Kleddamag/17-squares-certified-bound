from pathlib import Path
from fractions import Fraction as F
import json,hashlib,datetime,time
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import qr
R=Path(__file__).resolve().parent
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,q):p=Path(p);t=p.with_suffix('.tmp');t.write_text(json.dumps(q,indent=2));t.replace(p)
def rows(boxes):
 out=[];n=2*len(boxes)
 for i in range(len(boxes)):
  for j in range(i+1,len(boxes)):
   a=[F(0)]*n;b=F(-1);ds=[]
   for d in range(2):
    l=boxes[j][2*d]-boxes[i][2*d+1];u=boxes[j][2*d+1]-boxes[i][2*d];a[2*i+d]=l+u;a[2*j+d]=-l-u;b-=l*u;ds.append([l,u])
   out.append((a,b,[i,j],ds))
 return out
def exact_solve(M,y):
 T=[list(a)+[b] for a,b in zip(M,y)];n=len(y)
 for k in range(n):
  p=next(i for i in range(k,n) if T[i][k]);T[k],T[p]=T[p],T[k];v=T[k][k];T[k]=[x/v for x in T[k]]
  for i in range(n):
   if i!=k and T[i][k]:
    v=T[i][k];T[i]=[x-v*z for x,z in zip(T[i],T[k])]
 return [a[-1] for a in T]
def certify(boxes,ids,container,label,source):
 start=time.monotonic();rr=rows(boxes);n=2*len(boxes);bounds=[(b[k],b[k+1]) for b in boxes for k in [0,2]]
 B=np.array([[float(x) for x in a] for a,b,ij,ds in rr]);rhs=np.array([float(b) for a,b,ij,ds in rr]);bd=[(float(l),float(u)) for l,u in bounds]
 fit=linprog(np.r_[np.zeros(n),1.],A_ub=np.c_[B,-np.ones(len(rr))],b_ub=rhs,bounds=bd+[(0,None)],method='highs')
 q=dict(label=label,container=str(container),unit_side='1',cell_ids=ids,boxes=[[str(x) for x in b] for b in boxes],sources=source,rows=[dict(a=list(map(str,a)),b=str(b),pair=ij,difference_intervals=[[str(x) for x in z] for z in ds]) for a,b,ij,ds in rr],solver_status=int(fit.status),numerical_phase1=None if fit.fun is None else float(fit.fun),physical_square_packing=False)
 if fit.success and fit.fun>1e-8:
  lam=[max(F(0),F(round(-v*10**9),10**9)) for v in fit.ineqlin.marginals];coef=[sum(w*a[k] for w,(a,b,ij,ds) in zip(lam,rr)) for k in range(n)];right=sum(w*b for w,(a,b,ij,ds) in zip(lam,rr));left=sum(z*bounds[k][0 if z>=0 else 1] for k,z in enumerate(coef));margin=left-right
  support=sorted(set(j for w,(a,b,ij,ds) in zip(lam,rr) if w for j in ij))
  q.update(multipliers=list(map(str,lam)),exact_surplus=str(margin),support_square_indices=support,cut_cell_ids=[ids[j] for j in support],proved_exclusion=margin>0)
  q['status']='EXACT_JOINT_DISK_EXCLUSION' if margin>0 else 'FAILED_FLOAT_DUAL_PROPOSAL'
 elif fit.success:
  # Reconstruct a full-rank active basis of the linear relaxation, not a physical packing.
  sol=linprog(np.linspace(.001,.002,n),A_ub=B,b_ub=rhs,bounds=bd,method='highs');candidates=[];targets=[]
  for a,b,ij,ds in rr:
   if abs(float(b)-np.dot(list(map(float,a)),sol.x))<1e-6:candidates.append(a);targets.append(b)
  for k,(lo,hi) in enumerate(bounds):
   for v in [lo,hi]:
    if abs(float(v)-sol.x[k])<1e-6:
     a=[F(0)]*n;a[k]=F(1);candidates.append(a);targets.append(v)
  try:
   Q,T,piv=qr(np.array(candidates,dtype=float).T,pivoting=True);ix=piv[:n];x=exact_solve([candidates[k] for k in ix],[targets[k] for k in ix]);slacks=[b-sum(z*w for z,w in zip(a,x)) for a,b,ij,ds in rr];ok=all(lo<=v<=hi for v,(lo,hi) in zip(x,bounds)) and min(slacks)>=0
   if ok:q.update(rational_linear_centers=list(map(str,x)),minimum_linear_slack=str(min(slacks)),actual_minimum_squared_distance=str(min((x[2*i]-x[2*j])**2+(x[2*i+1]-x[2*j+1])**2 for i in range(len(boxes)) for j in range(i))),proved_exclusion=False,status='EXACT_LINEAR_RELAXATION_SURVIVOR')
   else:q.update(status='UNVERIFIED_PRIMAL_PROPOSAL',proved_exclusion=False)
  except Exception as e:q.update(status='PRIMAL_RECONSTRUCTION_FAILED',error=str(e),proved_exclusion=False)
 else:q.update(status='SOLVER_UNRESOLVED',proved_exclusion=False)
 q.update(seconds=time.monotonic()-start,utc=utc());return q
if __name__=='__main__':
 old=R.parent/'global-area/outputs';g=json.loads((old/'global-localization-test.json').read_text());p=json.loads((old/'global-rectangle-test.json').read_text());A=F(g['A']);ids=p['selection'];boxes=[[F(z)/A for z in g['boxes'][i]] for i in ids];q=certify(boxes,ids,F(g['target']),'round05-surviving-global-assignment',[dict(path=str(old/f),sha256=sha(old/f)) for f in ['global-localization-test.json','global-rectangle-test.json']]);save(R/'outputs/old-witness-joint.json',q);print(q['status'],q.get('exact_surplus'),q.get('cut_cell_ids'),flush=True)
