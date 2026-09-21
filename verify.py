#!/usr/bin/env python3
"""Replay the fixed global certificate with two independent exact geometries."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse, hashlib, json, os, subprocess, sys
from prepare_secondary import ensure_secondary

ROOT = Path(__file__).resolve().parent
SHA = '0288aaac680131aa675adb63ea6a67e3d363fcca6061d4c788301da7c5d69cec'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=2,
                    help='Workers per checker; both checkers run concurrently.')
    args = ap.parse_args()
    if sys.flags.optimize:
        raise ValueError('Run without Python optimization (-O).')
    if args.output.exists() or not 1 <= args.jobs <= 32:
        raise ValueError('Choose a new output directory and 1–32 workers.')
    cert = ROOT / 'global-certificate.json'
    raw = cert.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA:
        raise ValueError('Certificate hash mismatch.')
    c = json.loads(raw)
    if (c['A'], c['L'], len(c['entries']), c['budget_units'], c['minimum_units']) != (
            '99853/100000', '4613/1000', 7853, 16998427356, 1000020517):
        raise ValueError('Unexpected theorem data.')
    ensure_secondary()
    args.output.mkdir(parents=True)
    out = args.output.resolve()
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    commands = [
        ('python', [sys.executable, str(ROOT/'replay_parallel.py'), str(cert),
                    '--output', str(out/'python.json'), '--jobs', str(args.jobs)]),
        ('secondary', [sys.executable, str(ROOT/'replay_secondary_parallel.py'), str(cert),
                       '--output-dir', str(out/'secondary'), '--jobs', str(args.jobs)])]
    def run(item):
        name, command = item
        with (out/(name+'.log')).open('w') as log:
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                           env=env, check=True)
        print(name + ' complete', flush=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run, commands))
    x = json.loads((out/'python.json').read_text())
    y = json.loads((out/'secondary/RESULT.json').read_text())
    if x['status'] != 'PASS_FULL_EXACT_PYTHON_REPLAY' or y['status'] != 'PASS_FULL_EXACT_BIGINT_REPLAY':
        raise ValueError('A checker did not pass.')
    if x['intervals'] != 7853 or y['range'] != [0, 7853] or y['escape_rows']:
        raise ValueError('Incomplete replay.')
    for key in ('certificate_sha256', 'parent_side', 'budget_units', 'minimum_units', 'histogram'):
        if x[key] != y[key]:
            raise ValueError('Replays disagree: ' + key)
    if x['certificate_sha256'] != SHA or sum(x['histogram'].values()) != 7853:
        raise ValueError('Invalid replay identity/coverage.')
    gap = 17*x['minimum_units']-x['budget_units']
    if gap <= 0:
        raise ValueError('No counting contradiction.')
    result = {
        'status': 'PASS_TWO_COMPLETE_EXACT_REPLAYS',
        'strict_lower_bound': x['bound'], 'certificate_sha256': SHA,
        'intervals': 7853, 'minimum_charge_units': x['minimum_units'],
        'budget_units': x['budget_units'], 'counting_surplus_units': gap,
        'minimum_containment_margin': x['strict_core_margin'],
        'histograms_identical': True}
    (out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)

if __name__ == '__main__':
    main()
