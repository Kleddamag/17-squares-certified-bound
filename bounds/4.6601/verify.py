"""Fresh complete two-language replay of a supplied seventeen-square certificate."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import argparse,subprocess,sys,json,hashlib,datetime,concurrent.futures,shutil
if not __debug__:
 raise SystemExit("Run without -O/-OO and unset PYTHONOPTIMIZE.")
from pathlib import Path
from fractions import Fraction as F

def main():
 p=argparse.ArgumentParser();p.add_argument('certificate',nargs='?',default=str(Path(__file__).resolve().parent/'certificate.json'));p.add_argument('--target',default='46601/10000');p.add_argument('--output-directory',required=True);p.add_argument('--workers',type=int,default=1);a=p.parse_args()
 root=Path(__file__).resolve().parent;cert=Path(a.certificate).resolve();raw=cert.read_bytes();c=json.loads(raw);target=F(a.target);assert F(c['L'])/F(c['A'])==target;assert a.workers>=1
 assert F(c['normalized_target'])==target;node=root/'verify_global_variable.js'
 node_executable=shutil.which('node')
 if node_executable is None:raise SystemExit('Node.js must be installed and available on PATH.')
 out=Path(a.output_directory).resolve();out.mkdir(parents=True,exist_ok=False);N=len(c['entries']);assert N==2543
 commands=[[sys.executable,str(root/'verify_global_python.py'),str(cert),str(out/'python.json'),str(a.workers)]]
 for i in range(a.workers):
  lo=N*i//a.workers;hi=N*(i+1)//a.workers;commands.append([node_executable,str(node),str(cert),str(out/f'node-{i}.json'),str(lo),str(hi-lo),'audit'])
 def run(pair):
  i,cmd=pair
  with open(out/f'command-{i}.log','w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
  return dict(command=cmd,returncode=r.returncode)
 with concurrent.futures.ThreadPoolExecutor(max_workers=len(commands)) as pool:records=list(pool.map(run,enumerate(commands)))
 assert all(r['returncode']==0 for r in records),records
 py=json.load(open(out/'python.json'));jj=[json.load(open(out/f'node-{i}.json')) for i in range(a.workers)];rows=sum([d['rows'] for d in jj],[])
 assert [r['interval'] for r in rows]==list(range(N));assert [r['interval'] for r in py['rows']]==list(range(N));assert not py['failed_intervals'];digest=hashlib.sha256(raw).hexdigest();assert all(d['certificate_sha256']==digest for d in [py]+jj);assert all(int(r['minimum_units'])>=c['minimum_units'] for r in rows)
 for x,y in zip(py['rows'],rows):assert x['interval']==y['interval'] and x['minimum_units']==int(y['minimum_units']) and x['cells']==y['cells']
 gamma=min(r['minimum_units'] for r in py['rows']);M=c['budget_units'];assert 17*gamma>M
 result=dict(status='PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION',side_bound=f's(17)>{target}',target=str(target),certificate_sha256=digest,budget_units=M,minimum_units=gamma,surplus=17*gamma-M,ratio=str(F(M,gamma)),intervals=N,verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),processes=records)
 (out/'theorem.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
