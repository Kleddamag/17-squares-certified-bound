from pathlib import Path
from fractions import Fraction as F
import numpy as np,json,hashlib,datetime,time
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
R=Path(__file__).resolve().parent;src=R/'inputs/grid.json';rec=json.loads(src.read_text());E=[F(z,10**16) for z in rec['center_edges_integer'][::4]];A=F(461300,467001);L=F(4613,1000);N=16;boxes=[[E[x],E[x+1],E[y],E[y+1]] for x in range(N) for y in range(N)];conflicts=[]
for i,b in enumerate(boxes):
 assert (b[1]-b[0])**2+(b[3]-b[2])**2<A*A
 for j,c in enumerate(boxes[:i]):
  dx=max(abs(c[0]-b[1]),abs(c[1]-b[0]));dy=max(abs(c[2]-b[3]),abs(c[3]-b[2]))
  if dx*dx+dy*dy<A*A:conflicts.append([j,i])
old=R/'inputs/reference-case.json';case=json.loads(old.read_text());cells=[((i%4096)//64//4,(i%64)//4) for i in case['selected_domains']];patterns=[]
for reflection in [False,True]:
 for k in range(4):
  a=[(15-x if reflection else x,y) for x,y in cells]
  for _ in range(k):a=[(15-y,x) for x,y in a]
  ids=sorted(x*16+y for x,y in a);assert len(set(ids))==17
  if ids not in patterns:patterns.append(ids)
rows=[list(range(256))]+conflicts+patterns;ri=[];ci=[]
for r,ids in enumerate(rows):ri.extend([r]*len(ids));ci.extend(ids)
B=coo_matrix((np.ones(len(ri)),(np.array(ri,dtype=np.int32),np.array(ci,dtype=np.int32))),shape=(len(rows),256)).tocsc();lo=np.r_[17.,np.full(len(rows)-1,-np.inf)];hi=np.r_[17.,np.ones(len(conflicts)),np.full(len(patterns),16.)];start=time.monotonic();fit=milp(np.linspace(0,1e-5,256),integrality=np.ones(256),bounds=Bounds(np.zeros(256),np.ones(256)),constraints=LinearConstraint(B,lo,hi),options=dict(time_limit=45,mip_rel_gap=0.0));selection=[] if fit.x is None else np.flatnonzero(fit.x>.5).tolist()
valid=len(selection)==17 and all(not(i in selection and j in selection) for i,j in conflicts) and all(len(set(selection)&set(p))<=16 for p in patterns)
out=dict(status='RELAXED_LOCALIZATION_COUNTEREXAMPLE_PENDING_EXACT_CHECK' if valid else 'BOUNDED_GLOBAL_RELAXATION_TEST_UNRESOLVED',target='467001/100000',L=str(L),A=str(A),N=N,grid_source=str(src),grid_source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),center_edges=[str(x) for x in E],boxes=[[str(x) for x in b] for b in boxes],conflicts=conflicts,reference_source=str(old),reference_source_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),reference_D4_patterns=patterns,selection=selection,solver_status=int(fit.status),solver_message=fit.message,seconds=time.monotonic()-start,scope='A global center-cell relaxation witness outside8 reference coarse patterns; not a physical packing and not a counterexample to a possible stronger physical localization theorem.',hypothesis_test='Do inscribed-disk pair conflicts and exactly17 selected cells force one of the reference D4 center patterns?',artificial_test_constraints='Each of8 reference cell sets is forbidden only to search for a counterexample to localization of this RELAXATION; these exclusions are not asserted globally valid physical constraints.',utc=datetime.datetime.now(datetime.timezone.utc).isoformat());(R/'outputs/global-localization-test.json').write_text(json.dumps(out,indent=2));print(out['status'],'selected',selection,'conflicts',len(conflicts),'seconds',out['seconds'],flush=True)
