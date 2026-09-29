import json,sys,time,datetime,hashlib,multiprocessing as mp
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'global_src'))
from exact_general import validate,geometry
from integer_sweep import accumulate
DATA=None;MIN=None
def setup(data,minimum):
 global DATA,MIN;DATA=data;MIN=minimum

def one(job):
 i,v=job;arr=geometry(*DATA,*v);z,cells,win=accumulate(*arr);return dict(interval=i,minimum_units=int(z),cells=int(cells),passed=int(z)>=MIN)
if __name__=='__main__':
 start=time.monotonic();cp=Path(sys.argv[1]);c=json.loads(cp.read_text());data,jobs,margin=validate(c);rows=[]
 with mp.get_context('spawn').Pool(int(sys.argv[3]) if len(sys.argv)>3 else 2,setup,(data,c['minimum_units'])) as pool:
  for rec in pool.imap_unordered(one,enumerate(jobs),chunksize=4):
   rows.append(rec)
   if len(rows)%128==0:print('PYTHON_INTERVALS',len(rows),'minimum',min(v['minimum_units'] for v in rows),flush=True)
 rows.sort(key=lambda v:v['interval']);assert [v['interval'] for v in rows]==list(range(len(jobs)));failed=[r for r in rows if not r['passed']];out=dict(status='PASS_COMPLETE_EXACT_GLOBAL_THRESHOLD_COVER' if not failed else 'EXACT_GLOBAL_COVERAGE_FAILURE',intervals=len(rows),minimum_units=min(r['minimum_units'] for r in rows),budget_units=c['budget_units'],required_units=c['minimum_units'],failed_intervals=failed,rows=rows,certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),seconds=time.monotonic()-start,verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());Path(sys.argv[2]).write_text(json.dumps(out));print(json.dumps({k:v for k,v in out.items() if k not in ['rows','failed_intervals']}));sys.exit(2 if failed else 0)
