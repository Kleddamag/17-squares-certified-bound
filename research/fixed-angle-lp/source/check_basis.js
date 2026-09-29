// Independent Node BigInt replay; geometry rebuilt from vertex projections.
const fs=require('fs'), crypto=require('crypto'), path=require('path');
function assert(x,msg){if(!x)throw Error(msg);}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let c=a%b;a=b;b=c;}return a;}
class Q{
 constructor(a,b=1n){a=BigInt(a);b=BigInt(b);assert(b!==0n,'zero denominator');if(b<0n){a=-a;b=-b;}let g=gcd(a,b);this.a=a/g;this.b=b/g;}
 static read(s){let p=String(s).split('/');return new Q(p[0],p[1]||'1');}
 add(x){return new Q(this.a*x.b+x.a*this.b,this.b*x.b);}
 sub(x){return new Q(this.a*x.b-x.a*this.b,this.b*x.b);}
 mul(x){return new Q(this.a*x.a,this.b*x.b);}
 div(x){return new Q(this.a*x.b,this.b*x.a);}
 neg(){return new Q(-this.a,this.b);}
 cmp(x){let a=this.a*x.b-x.a*this.b;return a<0n?-1:a>0n?1:0;}
 str(){return this.b===1n?String(this.a):`${this.a}/${this.b}`;}
}
const zero=new Q(0),one=new Q(1),two=new Q(2);
const sum=a=>a.reduce((s,x)=>s.add(x),zero),dot=(a,b)=>sum(a.map((x,i)=>x.mul(b[i])));
function min(a){return a.reduce((x,y)=>x.cmp(y)<=0?x:y);}
function max(a){return a.reduce((x,y)=>x.cmp(y)>=0?x:y);}
function hash(p){return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');}
function geometry(t){let tt=t.mul(t),den=one.add(tt),c=one.sub(tt).div(den),s=two.mul(t).div(den);let u=[c,s],v=[s.neg(),c];let points=[];for(let a of [-1,1])for(let b of [-1,1])points.push(u.map((x,k)=>x.mul(new Q(a)).add(v[k].mul(new Q(b))).div(two)));return {u,v,points};}
function pointkeys(g){return g.points.map(p=>p.map(x=>x.str()).join(',')).sort().join('|');}
function support(points,n){return max(points.map(p=>dot(n,p)));}
function rankdet(A){let a=A.map(r=>r.slice()),det=one,N=a.length;for(let k=0;k<N;k++){let r=k;while(r<N&&a[r][k].a===0n)r++;assert(r<N,'singular basis');if(r!==k){[a[k],a[r]]=[a[r],a[k]];det=det.neg();}let p=a[k][k];det=det.mul(p);for(let j=k;j<N;j++)a[k][j]=a[k][j].div(p);for(let i=k+1;i<N;i++){let q=a[i][k];if(q.a!==0n)for(let j=k;j<N;j++)a[i][j]=a[i][j].sub(q.mul(a[k][j]));}}return det;}
const certPath=process.argv[2]||path.join(__dirname,'../evidence/basis-certificate.json');
const outputPath=process.argv[3]||path.join(__dirname,'../evidence/basis-replay-node.json');
const start=new Date().toISOString(),cert=JSON.parse(fs.readFileSync(certPath,'utf8')),input=JSON.parse(fs.readFileSync(cert.input_path,'utf8'));
assert(hash(cert.input_path)===cert.input_sha256,'input hash mismatch');
assert(cert.schema==='s17-fixed-angle-optimal-basis-v1','schema');
assert(input.squares.length===17&&cert.permutation.length===17&&new Set(cert.permutation).size===17,'permutation');
const U=Q.read(input.side),geom=[],originalZ=[];
for(let k=0;k<17;k++){
 let id=cert.permutation[k];assert(Number.isInteger(id)&&id>=0&&id<17,'bad original label');let s=input.squares[id],old=Q.read(s.t),t=Q.read(cert.canonical_t[k]);assert(t.cmp(zero)>=0&&t.cmp(one)<=0,'canonical interval');
 if(k)assert(Q.read(cert.canonical_t[k-1]).cmp(t)<=0,'angle order');
 let g=geometry(t);assert(pointkeys(g)===pointkeys(geometry(old)),'canonicalization changes square');geom.push(g);originalZ.push(Q.read(s.x),Q.read(s.y));
}
originalZ.push(U);
const rows=[],walls=new Set(),pairs=new Set();
assert(cert.selected_rows.length===204,'row inventory');
for(let d of cert.selected_rows){
 let a=Array(35).fill(zero),b;
 if(d.kind==='wall'){
  assert(Number.isInteger(d.i)&&d.i>=0&&d.i<17&&[0,1].includes(d.coordinate)&&typeof d.upper==='boolean','wall descriptor');
  let key=`${d.i}/${d.coordinate}/${d.upper}`;assert(!walls.has(key),'duplicate wall');walls.add(key);
  a[2*d.i+d.coordinate]=d.upper?one.neg():one;if(d.upper)a[34]=one;
  let n=d.coordinate===0?[one,zero]:[zero,one];b=support(geom[d.i].points,n);
 }else{
  assert(d.kind==='pair'&&Number.isInteger(d.i)&&Number.isInteger(d.j)&&0<=d.i&&d.i<d.j&&d.j<17&&[d.i,d.j].includes(d.owner)&&[0,1].includes(d.axis)&&[-1,1].includes(d.sign),'pair descriptor');
  let key=`${d.i}/${d.j}`;assert(!pairs.has(key),'duplicate pair');pairs.add(key);
  let n=(d.axis===0?geom[d.owner].u:geom[d.owner].v).map(x=>x.mul(new Q(d.sign)));
  for(let k=0;k<2;k++){a[2*d.i+k]=n[k].neg();a[2*d.j+k]=n[k];}
  b=support(geom[d.i].points,n).add(support(geom[d.j].points,n));
 }
 assert(dot(a,originalZ).cmp(b)>=0,'selected LP does not contain original cap');rows.push({a,b});
}
assert(walls.size===68&&pairs.size===136,'incomplete row coverage');
const ids=cert.basis_indices,z=cert.z.map(Q.read),lambda=cert.lambda.map(Q.read);
assert(ids.length===35&&new Set(ids).size===35&&z.length===35&&lambda.length===35,'basis shapes');
assert(ids.every(i=>Number.isInteger(i)&&i>=0&&i<204),'basis row labels');
let A=ids.map(i=>rows[i].a),b=ids.map(i=>rows[i].b),det=rankdet(A);
assert(det.cmp(Q.read(cert.determinant))===0,'determinant mismatch');
for(let k=0;k<35;k++)assert(dot(A[k],z).cmp(b[k])===0,'basis equality');
for(let k=0;k<35;k++){assert(lambda[k].cmp(zero)>=0,'negative dual');let balanced=sum(A.map((row,j)=>row[k].mul(lambda[j])));assert(balanced.cmp(k===34?one:zero)===0,'dual balance');}
assert(dot(lambda,b).cmp(z[34])===0,'dual objective mismatch');
const slacks=rows.map(r=>dot(r.a,z).sub(r.b));assert(min(slacks).cmp(zero)>=0,'LP primal violation');assert(z[34].cmp(U)<=0,'cap increased');
let wallClear=[],pairClear=[];
let points=geom.map((g,i)=>g.points.map(q=>[q[0].add(z[2*i]),q[1].add(z[2*i+1])]));
for(let ps of points)for(let p of ps)for(let q of p){assert(q.cmp(zero)>=0&&q.cmp(z[34])<=0,'physical wall violation');wallClear.push(q,z[34].sub(q));}
for(let i=0;i<17;i++)for(let j=i+1;j<17;j++){
 let gaps=[];for(let n of [geom[i].u,geom[i].v,geom[j].u,geom[j].v]){let p=points[i].map(v=>dot(n,v)),q=points[j].map(v=>dot(n,v));gaps.push(min(q).sub(max(p)),min(p).sub(max(q)));}
 let gap=max(gaps);assert(gap.cmp(zero)>=0,'physical pair overlap');pairClear.push(gap);
}
let receipt={status:'PASS_INDEPENDENT_EXACT_BASIS_PRIMAL_DUAL_GEOMETRY',start_utc:start,completion_utc:new Date().toISOString(),certificate_sha256:hash(certPath),checker_sha256:hash(__filename),input_sha256:hash(cert.input_path),variables:35,selected_rows:204,basis_rank:35,unit_squares:17,pairs:136,vertices:68,positive_duals:lambda.filter(x=>x.a>0n).length,zero_duals:lambda.filter(x=>x.a===0n).length,side:z[34].str(),lp_primal_min:min(slacks).str(),dual_min:min(lambda).str(),wall_clearance_min:min(wallClear).str(),pair_clearance_min:min(pairClear).str(),original_cap_admitted:true,scope:'optimum of selected-separator LP at these fixed rational angles; not optimum over separators or independent angles'};
fs.writeFileSync(outputPath,JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify({status:receipt.status,basis_rank:35,positive_duals:receipt.positive_duals,zero_duals:receipt.zero_duals,pairs:136}));
