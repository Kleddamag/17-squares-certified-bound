"""Exhaustive finite-rule checks and targeted corruption/sweep controls.

These supplement, and do not replace, the complete geometric replay.
Adapted from this project's completed weighted_controls.py audit.
"""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import argparse, copy, datetime, hashlib, json, shutil, subprocess, sys
from fractions import Fraction as F
from pathlib import Path

if not __debug__:
    raise SystemExit('Run without -O/-OO and unset PYTHONOPTIMIZE.')
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'global_src'))
from exact_general import validate, geometry
from integer_sweep import accumulate
from boolean_rule import expansion

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-directory', required=True)
    args = parser.parse_args()
    out = Path(args.output_directory).resolve()
    out.mkdir(parents=True, exist_ok=False)
    node = shutil.which('node')
    if node is None:
        raise SystemExit('Node.js must be available on PATH.')
    path = ROOT/'certificate.json'
    cert = json.loads(path.read_text())
    data, jobs, margin = validate(cert)
    assert F(cert['L'])/F(cert['A']) == F(cert['normalized_target']) == F(232001, 50000)
    patterns = {}
    for group in cert['threshold_orbits']:
        coefficients = tuple(group.get('coefficients', [1]*len(group['sets'][0])))
        threshold = group['threshold']
        rules = tuple(group.get('winning_masks', ()))
        key = (coefficients, threshold, rules)
        if key in patterns:
            continue
        terms = expansion(coefficients, threshold, rules)
        n = len(coefficients)
        wins = []
        for mask in range(1 << n):
            expected = int(any(mask & w == w for w in rules)) if rules else int(sum(a for j, a in enumerate(coefficients) if mask >> j & 1) >= threshold)
            actual = sum(a for subset, a in terms if all(mask >> j & 1 for j in subset))
            assert actual == expected
            if expected:
                wins.append(mask)
        dp = [0]*(1 << n)
        for mask in range(1 << n):
            for hit in wins:
                if mask & hit == hit:
                    dp[mask] = max(dp[mask], 1 + dp[mask ^ hit])
        budget = 1 if rules else sum(coefficients)//threshold
        assert dp[-1] <= budget
        patterns[key] = dict(coefficients=coefficients, threshold=threshold, winning_masks=rules, boolean_patterns=1 << n, maximum_disjoint_winners=dp[-1], budget=budget)
    direct = []
    for interval in [0, 511, 1024, 2047]:
        arrays = geometry(*data, *jobs[interval])
        fast = accumulate(*arrays)
        reference = accumulate(*arrays, direct=True)
        assert tuple(fast) == tuple(reference)
        receipt = out/f'positive-node-{interval}.json'
        process = subprocess.run([node, str(ROOT/'verify_global_variable.js'), str(path), str(receipt), str(interval), '1', 'audit'], capture_output=True, text=True)
        assert process.returncode == 0, process.stderr
        row = json.loads(receipt.read_text())['rows'][0]
        assert int(row['minimum_units']) == int(fast[0]) and row['cells'] == int(fast[1])
        direct.append(dict(interval=interval, minimum=int(fast[0]), cells=int(fast[1]), node_matched=True))
    weighted = next(i for i, g in enumerate(cert['threshold_orbits']) if g.get('coefficients'))
    games = [i for i, g in enumerate(cert['threshold_orbits']) if g.get('winning_masks')]
    negatives = []
    names = ['budget', 'zero-coefficient', 'wrong-coefficient', 'missing-image', 'angle-gap', 'non-strict-core', 'false-target']
    if games:
        names.append('disjoint-rule-winners')
    for name in names:
        bad = copy.deepcopy(cert)
        if name == 'budget': bad['budget_units'] += 1
        elif name == 'zero-coefficient': bad['threshold_orbits'][weighted]['coefficients'][0] = 0
        elif name == 'wrong-coefficient': bad['threshold_orbits'][weighted]['coefficients'][0] += 7
        elif name == 'missing-image': bad['threshold_orbits'][weighted]['sets'].pop()
        elif name == 'angle-gap': bad['entries'][0][0] = '1/100000'
        elif name == 'non-strict-core': bad['entries'][0][3] = bad['A']
        elif name == 'false-target': bad['normalized_target'] = '465/100'
        elif name == 'disjoint-rule-winners': bad['threshold_orbits'][games[0]]['winning_masks'] = [1, 2]
        try:
            assert F(bad['L'])/F(bad['A']) == F(bad['normalized_target']) == F(232001, 50000), 'target identity'
            validate(bad)
        except (ValueError, AssertionError, KeyError) as error:
            rejection = str(error)
        else:
            raise AssertionError('Python accepted ' + name)
        bad_path = out/f'negative-{name}.json'
        bad_path.write_text(json.dumps(bad))
        process = subprocess.run([node, str(ROOT/'verify_global_variable.js'), str(bad_path), str(out/f'negative-{name}-node.json'), '0', '1', 'audit'], capture_output=True, text=True)
        assert process.returncode != 0, 'Node accepted ' + name
        assert 'Error:' in process.stderr and 'Cannot find module' not in process.stderr
        negatives.append(dict(name=name, python_rejection=rejection, node_exit=process.returncode))
    result = dict(status='PASS_RULE_BUDGET_SWEEP_AND_NEGATIVE_CONTROLS', certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), minimum_strict_margin=str(margin), patterns=list(patterns.values()), direct_sweeps=direct, negative_controls=negatives, verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    (out/'controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
