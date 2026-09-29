"""Own-code fixed-angle LP proposal and exact reconstruction. Float discovery only."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,time,itertools
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'data/upper-packing-certificate.json'

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def axis(t):
    c,s=(1-t*t)/(1+t*t),2*t/(1+t*t)
    return (c,s),(-s,c)
def canon(t):
    # This input has |t|<1, so add a quarter turn precisely when negative.
    assert -1<t<1
    return (t+1)/(1-t) if t<0 else t
def solve(A,b):
    a=[list(row)+[bb] for row,bb in zip(A,b)]; N=len(A); det=F(1)
    for k in range(N):
        pivot=next((r for r in range(k,N) if a[r][k]),None)
        if pivot is None: raise ValueError('singular basis')
        if pivot!=k: a[k],a[pivot]=a[pivot],a[k]; det=-det
        p=a[k][k]; det*=p
        a[k]=[x/p for x in a[k]]
        for r in range(k+1,N):
            q=a[r][k]
            if q:
                a[r]=[x-q*y for x,y in zip(a[r],a[k])]
    x=[F(0)]*N
    for k in range(N-1,-1,-1): x[k]=a[k][-1]-dot(a[k][k+1:N],x[k+1:])
    return x,det
def independent(rows,indices):
    pivots={}; chosen=[]
    for idx in indices:
        v=list(rows[idx][0])
        for k,row in sorted(pivots.items()):
            if v[k]:
                q=v[k]; v=[x-q*y for x,y in zip(v,row)]
        k=next((k for k,x in enumerate(v) if x),None)
        if k is not None:
            q=v[k]; pivots[k]=[x/q for x in v]; chosen.append(idx)
        if len(chosen)==35: return chosen
    return chosen

def main():
    start=time.time(); data=json.loads(INPUT.read_text()); U=F(data['side'])
    sq=[(i,F(e['x']),F(e['y']),canon(F(e['t']))) for i,e in enumerate(data['squares'])]
    sq.sort(key=lambda q:(q[3],q[0])); axes=[axis(q[3]) for q in sq]
    z0=[v for _,x,y,t in sq for v in (x,y)]+[U]
    rows=[]
    for i,(_,x,y,t) in enumerate(sq):
        h=sum(axes[i][0])/2
        for coord,sign,top in ((0,1,False),(1,1,False),(0,-1,True),(1,-1,True)):
            a=[F(0)]*35; a[2*i+coord]=F(sign); a[-1]=F(int(top))
            desc={'kind':'wall','i':i,'coordinate':coord,'upper':top}
            rows.append((a,h,desc))
    for i,j in itertools.combinations(range(17),2):
        candidates=[]
        for owner in (i,j):
            for k in (0,1):
                for sign in (-1,1):
                    n=tuple(sign*x for x in axes[owner][k]); a=[F(0)]*35
                    for coord in (0,1): a[2*i+coord]=-n[coord]; a[2*j+coord]=n[coord]
                    b=sum(abs(dot(n,ax)) for who in (i,j) for ax in axes[who])/2
                    # Independently assert ordered-angle closed-form support.
                    ui,uj=axes[i][0],axes[j][0]
                    expected=(1+dot(ui,uj)+ui[0]*uj[1]-ui[1]*uj[0])/2
                    assert b==expected
                    d={'kind':'pair','i':i,'j':j,'owner':owner,'axis':k,'sign':sign}
                    candidates.append((dot(a,z0)-b,a,b,d))
        gap,a,b,d=max(candidates,key=lambda q:q[0]); assert gap>=0
        rows.append((a,b,d))
    assert len(rows)==204 and all(dot(a,z0)>=b for a,b,d in rows)
    af=np.array([[float(x) for x in a] for a,b,d in rows]); bf=np.array([float(b) for a,b,d in rows]); c=np.zeros(35); c[-1]=1
    res=linprog(c,A_ub=-af,b_ub=-bf,bounds=[(None,None)]*35,method='highs-ds',options={'time_limit':60.0,'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    numerical={'status':int(res.status),'message':str(res.message),'side':float(res.fun) if res.success else None,'seconds':time.time()-start}
    (ROOT/'evidence/numerical-proposal.json').write_text(json.dumps(numerical,indent=2)+'\n')
    assert res.success, numerical
    slacks=af@res.x-bf; weights=-res.ineqlin.marginals
    active=[k for k,s in enumerate(slacks) if abs(s)<1e-7]
    support=[k for k in active if weights[k]>1e-8]
    priority=sorted(support,key=lambda k:-weights[k])+[k for k in active if k not in support]
    basis=independent(rows,priority); assert len(basis)==35
    A=[rows[k][0] for k in basis]; b=[rows[k][1] for k in basis]
    z,det=solve(A,b); dual,_=solve(list(map(list,zip(*A))),[F(0)]*34+[F(1)])
    primal=[dot(a,z)-bb for a,bb,d in rows]
    # Exact primal simplex on the dual LP. Floating discovery may choose
    # incorrect zero-force rows when rounded rational gaps are tiny.
    assert min(dual)>=0, ('initial dual infeasible',min(dual))
    pivots=[]
    for step in range(200):
        entering=next((k for k,v in enumerate(primal) if v<0),None)
        if entering is None: break
        coeff,_=solve(list(map(list,zip(*A))),rows[entering][0])
        eligible=[k for k,v in enumerate(coeff) if v>0]
        assert eligible, 'selected LP unexpectedly infeasible'
        leaving=min(eligible,key=lambda k:(dual[k]/coeff[k],basis[k]))
        pivots.append({'entering':entering,'leaving':basis[leaving],'old_violation':str(primal[entering]),'dual_step':str(dual[leaving]/coeff[leaving])})
        basis[leaving]=entering
        A=[rows[k][0] for k in basis]; b=[rows[k][1] for k in basis]
        z,det=solve(A,b); dual,_=solve(list(map(list,zip(*A))),[F(0)]*34+[F(1)])
        primal=[dot(a,z)-bb for a,bb,d in rows]
        assert min(dual)>=0
        (ROOT/'evidence/exact-pivots.json').write_text(json.dumps({'steps':pivots,'basis':basis,'primal_min':str(min(primal)),'complete':min(primal)>=0},indent=2)+'\n')
    assert min(primal)>=0, 'exact pivot cap reached'
    cert={'schema':'s17-fixed-angle-optimal-basis-v1','input_path':'data/upper-packing-certificate.json','input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'permutation':[q[0] for q in sq],'canonical_t':[str(q[3]) for q in sq],'selected_rows':[d for a,b,d in rows],'basis_indices':basis,'z':[str(x) for x in z],'lambda':[str(x) for x in dual],'determinant':str(det),'primal_min':str(min(primal)),'dual_min':str(min(dual)),'side_display':float(z[-1]),'fixed_angle_optimum_claim':min(primal)>=0 and min(dual)>=0,'numerical':numerical,'exact_support_indices':[basis[k] for k,x in enumerate(dual) if x>0],'zero_dual_count':sum(x==0 for x in dual),'exact_pivot_count':len(pivots),'elapsed_seconds':time.time()-start}
    (ROOT/'evidence/basis-certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    assert min(primal)>=0, ('bad primal',min(primal))
    assert min(dual)>=0, ('bad dual',min(dual))
    assert dot(dual,b)==z[-1] and z[-1]<=U
    upper={'description':'Exact optimum of one selected-separator LP with fixed accepted orientations; not a global optimum claim','side':str(z[-1]),'squares':[{'x':str(z[2*i]),'y':str(z[2*i+1]),'t':str(q[3])} for i,q in enumerate(sq)]}
    (ROOT/'evidence/basis-packing.json').write_text(json.dumps(upper,indent=2)+'\n')
    print(json.dumps({'status':'PASS_EXACT_PROPOSER','side_display':float(z[-1]),'primal_min':str(min(primal)),'dual_min':str(min(dual)),'support_count':len(cert['exact_support_indices']),'zero_duals':cert['zero_dual_count'],'seconds':time.time()-start}))

if __name__=='__main__': main()
