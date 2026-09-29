from joint_disk import *
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
U=F(4675530093604551,10**15);N=16;E=[F(1,2)+(U-1)*i/N for i in range(N+1)];boxes=[[E[x],E[x+1],E[y],E[y+1]] for x in range(N) for y in range(N)];H=F(707107,10**6);conflicts=[];rects=[];rows_idx=[list(range(256))];upper=[17];cuts=[]
for i,b in enumerate(boxes):
 assert (b[1]-b[0])**2+(b[3]-b[2])**2<1
 for j,c in enumerate(boxes[:i]):
  dx=max(abs(c[0]-b[1]),abs(c[1]-b[0]));dy=max(abs(c[2]-b[3]),abs(c[3]-b[2]))
  if dx*dx+dy*dy<1:conflicts.append([j,i])
rows_idx+=conflicts;upper+=[1]*len(conflicts)
for x0 in range(N):
 for x1 in range(x0+1,N+1):
  w=min(U,E[x1]+H)-max(F(0),E[x0]-H)
  for y0 in range(N):
   for y1 in range(y0+1,N+1):
    h=min(U,E[y1]+H)-max(F(0),E[y0]-H);area=w*h;cap=area.numerator//area.denominator;ids=[x*N+y for x in range(x0,x1) for y in range(y0,y1)];rects.append(dict(window=[x0,x1,y0,y1],capacity=cap,area=str(area)))
    if cap<min(17,len(ids)):rows_idx.append(ids);upper.append(cap)
cap_src=R/'inputs/feasible-cap-control.json';cap=json.loads(cap_src.read_text());A=F(cap['side']);centers=[[F(p[0])/A,F(p[1])/A] for p in cap['poses']]
def cellof(p):
 ij=[min(N-1,max(i for i in range(N) if E[i]<=p[d])) for d in [0,1]];return ij[0]*N+ij[1]
cap_ids=[cellof(p) for p in centers];assert len(set(cap_ids))==17
for ids,b in zip(rows_idx,upper):assert len(set(cap_ids)&set(ids))<=b
model=dict(status='GLOBAL_NECESSARY_CENTER_COVER_AT_CAP',unit_side='1',container=str(U),side_scope='All physical unit-square packings with enclosing side S <= U; contain them in [0,U]^2 without moving squares.',N=N,center_edges=list(map(str,E)),boxes=[list(map(str,b)) for b in boxes],radius_upper=str(H),conflicts=conflicts,rectangles=rects,active_rectangle_rows=len(rows_idx)-1-len(conflicts),artificial_constraints=[],cap_control=dict(source=str(cap_src),sha256=sha(cap_src),cell_ids=cap_ids,centers=[[str(x) for x in p] for p in centers]),utc=utc());save(R/'outputs/cap-global-model.json',model)
# Every accepted learned cut is exact-checked in Python before entering the master. Solver status never proves global infeasibility.
start=time.monotonic();history=[]
for it in range(20):
 if time.monotonic()-start>240:break
 ri=[];ci=[]
 for k,ids in enumerate(rows_idx):ri.extend([k]*len(ids));ci.extend(ids)
 B=coo_matrix((np.ones(len(ri)),(np.array(ri,dtype=np.int32),np.array(ci,dtype=np.int32))),shape=(len(rows_idx),256)).tocsc()
 fit=milp(np.zeros(256),integrality=np.ones(256),bounds=Bounds(np.zeros(256),np.ones(256)),constraints=LinearConstraint(B,np.r_[17.,np.full(len(rows_idx)-1,-np.inf)],np.array(upper)),options=dict(time_limit=min(30,max(1,240-(time.monotonic()-start))),mip_rel_gap=0.0))
 ids=[] if fit.x is None else np.flatnonzero(fit.x>.5).tolist();chosen=set(ids);valid=len(ids)==17 and all(len(chosen&set(row))<=cap for row,cap in zip(rows_idx,upper));event=dict(iteration=it,solver_status=int(fit.status),solver_message=fit.message,selection=ids,exact_master_selection=valid)
 if not valid:history.append(event);save(R/'outputs/master-progress.json',dict(history=history,cuts=cuts,global_infeasibility_proved=False,utc=utc()));break
 q=certify([boxes[i] for i in ids],ids,U,f'cap-master-{it:03}',[dict(path=str(R/'outputs/cap-global-model.json'),sha256=sha(R/'outputs/cap-global-model.json'))]);p=R/'outputs'/f'joint-{it:03}.json';save(p,q);event.update(joint_certificate=str(p),joint_sha256=sha(p),joint_status=q['status']);history.append(event)
 if q['proved_exclusion']:
  cut=q['cut_cell_ids'];assert len(set(cap_ids)&set(cut))<=len(cut)-1;rows_idx.append(cut);upper.append(len(cut)-1);cuts.append(dict(cell_ids=cut,capacity=len(cut)-1,certificate=str(p),sha256=sha(p)))
 save(R/'outputs/master-progress.json',dict(history=history,cuts=cuts,global_infeasibility_proved=False,utc=utc()))
 print(it,q['status'],len(q.get('cut_cell_ids',[])),q.get('exact_surplus'),flush=True)
 if not q['proved_exclusion']:break
print('DONE',len(history),'proposals',len(cuts),'cuts',flush=True)
