"""Orchestrate complete disjoint ranges of the independent BigInt scanner."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,subprocess,json,hashlib,time
from prepare_secondary import ensure_secondary

def main():
 ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--output-dir',required=True);ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args();root=Path(__file__).resolve().parent;scanner=ensure_secondary();raw=Path(a.certificate).read_bytes();c=json.loads(raw);sha=hashlib.sha256(raw).hexdigest();n=len(c['entries']);out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();assert 0<a.jobs<=n
 ranges=[(j*n//a.jobs,(j+1)*n//a.jobs) for j in range(a.jobs)]
 def run(span):
  lo,hi=span;cmd=['node',str(scanner),'--certificate',str(Path(a.certificate).resolve()),'--expected-sha',sha,'--A',c['A'],'--start',str(lo),'--stop',str(hi)];r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE);(out/f'range-{lo}-{hi}.json').write_text(r.stdout);(out/f'range-{lo}-{hi}.stderr.txt').write_text(r.stderr);r.check_returncode();d=json.loads(r.stdout);assert d['range']==[lo,hi] and d['certificate_sha256']==sha and not d['escape_rows'];assert d['budget_units']==c['budget_units'] and d['minimum_units']>=c['minimum_units'];assert sum(d['histogram'].values())==hi-lo;return d
 with ThreadPoolExecutor(max_workers=a.jobs) as pool:parts=list(pool.map(run,ranges))
 hist={}
 for d in parts:
  for key,count in d['histogram'].items():hist[key]=hist.get(key,0)+count
 assert sum(hist.values())==n and ranges[0][0]==0 and ranges[-1][1]==n and all(x[1]==y[0] for x,y in zip(ranges,ranges[1:]));result={'status':'PASS_FULL_EXACT_BIGINT_REPLAY','certificate_sha256':sha,'parent_side':c['A'],'range':[0,n],'ranges':[list(x) for x in ranges],'budget_units':c['budget_units'],'minimum_units':min(d['minimum_units'] for d in parts),'histogram':hist,'center_slabs':sum(d['center_slabs'] for d in parts),'escape_rows':[],'seconds':time.monotonic()-start};(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='histogram'},indent=2),flush=True)
if __name__=='__main__':main()
