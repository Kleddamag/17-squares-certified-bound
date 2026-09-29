from pathlib import Path
from fractions import Fraction as F
import json,hashlib,datetime,time,numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
R=Path(__file__).resolve().parent;src=R/'outputs/global-localization-test.json';q=json.loads(src.read_text());E=list(map(F,q['center_edges']));A=F(q['A']);L=F(q['L']);r=F(707107,1000000);assert 2*r*r>=1;H=A*r;rectangles=[];constraints=[];caps=[];start=time.monotonic()
for x0 in range(16):
 for x1 in range(x0+1,17):
  w=min(L,E[x1]+H)-max(F(0),E[x0]-H)
  for y0 in range(16):
   for y1 in range(y0+1,17):
    h=min(L,E[y1]+H)-max(F(0),E[y0]-H);ratio=w*h/(A*A);cap=ratio.numerator//ratio.denominator;ids=[x*16+y for x in range(x0,x1) for y in range(y0,y1)];row=dict(x0=x0,x1=x1,y0=y0,y1=y1,capacity=cap,area_upper=str(w*h));rectangles.append(row)
    if cap<min(17,len(ids)):constraints.append(ids);caps.append(cap)
old_selection=set(q['selection']);violations=[v for v in rectangles if sum(v['x0']<=i//16<v['x1'] and v['y0']<=i%16<v['y1'] for i in old_selection)>v['capacity']];rows=[list(range(256))]+q['conflicts']+q['reference_D4_patterns']+constraints;upper=[17]+[1]*len(q['conflicts'])+[16]*len(q['reference_D4_patterns'])+caps;ri=[];ci=[]
for idx,ids in enumerate(rows):ri.extend([idx]*len(ids));ci.extend(ids)
B=coo_matrix((np.ones(len(ri)),(np.array(ri,dtype=np.int32),np.array(ci,dtype=np.int32))),shape=(len(rows),256)).tocsc();fit=milp(np.zeros(256),integrality=np.ones(256),bounds=Bounds(np.zeros(256),np.ones(256)),constraints=LinearConstraint(B,np.r_[17.,np.full(len(rows)-1,-np.inf)],np.array(upper)),options=dict(time_limit=40,mip_rel_gap=0.0));selected=[] if fit.x is None else np.flatnonzero(fit.x>.5).tolist();chosen=set(selected);valid=len(chosen)==17 and all(not(i in chosen and j in chosen) for i,j in q['conflicts']) and all(len(chosen.intersection(p))<=16 for p in q['reference_D4_patterns']) and all(sum(i in chosen for i in ids)<=cap for ids,cap in zip(constraints,caps))
out=dict(status='EXACT_RECTANGLE_CAPACITIES_AND_RELAXED_SURVIVOR_PENDING_REPLAY' if valid else 'EXACT_RECTANGLE_CAPACITIES_WITH_UNRESOLVED_SEARCH',target=q['target'],L=str(L),A=str(A),radius_factor=str(r),source=str(src),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),rectangles=rectangles,active_capacity_rows=len(constraints),old_selection_violations=violations,selection=selected,solver_status=int(fit.status),solver_message=fit.message,seconds=time.monotonic()-start,physical_packing=False,global_model_solved=False,utc=datetime.datetime.now(datetime.timezone.utc).isoformat());(R/'outputs/global-rectangle-test.json').write_text(json.dumps(out,indent=2));print(out['status'],'rectangles',len(rectangles),'active',len(constraints),'old violations',len(violations),'selected',selected,'seconds',out['seconds'],flush=True)
