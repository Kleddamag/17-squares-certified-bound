# Completed verification and release changes

The certificate SHA-256 is
`0288aaac680131aa675adb63ea6a67e3d363fcca6061d4c788301da7c5d69cec`.
All theorem statements refer to these exact bytes.

## Results

| Obligation | Completed result |
|---|---|
| Complete Python geometric sweep | All 7,853 intervals pass |
| Complete JavaScript BigInt geometry | All 7,853 intervals pass; no escape rows |
| Agreement | Identical full histograms; minimum 1,000,020,517 units |
| Counting | Budget 16,998,427,356; surplus 1,921,433 units |
| Strict containment | Minimum margin 1/10^12 |
| Independent containment audit | All 31,412 rational quadratic inequalities pass |
| Direct logical boundary controls | 3,403 tested centres pass |
| Structural audit | D4 symmetry, indexing, budgets and accumulator bounds pass |
| Retained upper packing | 17 unit squares, 68 vertices and 136 pairs pass |

Weights have denominator 10^9. The proof gives a universal boundary argument;
the finite boundary controls are additional implementation checks. The sweep
certifies 1,641,130,192,125 reachable open cells using range-minimum queries,
without individually enumerating those cells.

## Evidence map

- `RESULT.json` and `evidence/release-replay/RESULT.json`: fresh full replay
  through the publication launcher.
- `evidence/release-replay/python.json`: all interval results from that replay.
- `evidence/release-replay/secondary/`: all disjoint BigInt replay ranges and
  their combined result.
- `evidence/average4-adaptive-r1.python-replay.json` and
  `evidence/secondary-replay/`: the original complete exact checks.
- `evidence/packaged-replay/`: the earlier portable-package complete replay.
- `evidence/average4-global-independent-controls.json` and
  `evidence/packaged-independent-controls.json`: independently written
  containment and logical boundary checks, repeated after packaging.
- `evidence/average4-global-schema-independent-audit.json`: independent
  structural audit.
- `evidence/upper-replay.json`: unchanged rational packing verification.
- `evidence/theorem-file-identities.json`: hashes of unchanged theorem inputs
  and checker files, including the reconstructed secondary implementation.
- `evidence/release-environment.json`: versions used for the fresh release run.
- `evidence/prior-preservation.json`: the earlier certificate/archive remained
  unchanged in the research workspace. It is a historical preservation record,
  not an additional premise of the new theorem.

The schema audit can also be repeated with standard-library Python:

```sh
python3 audits/audit_candidate_schema.py global-certificate.json
```

It writes its report beside the audit script. `independent_controls.py`
reproduces the universal containment and selected boundary checks as documented
in the README.

## What changed for publication

The certificate, Python geometric engine, integer accumulator, independent
controls and upper-packing checker retain their completed-verification bytes.
Documentation was edited for a public release, GitHub math formatting and an
accurate human/AI contribution statement. Experimental research was removed
from the publication scope.

The secondary checker is prepared by a new SHA-pinned download/adaptation
wrapper. Its reconstructed bytes exactly match the earlier verified file.
The launcher was changed only to locate and prepare that checker. These
packaging changes received a fresh complete replay of both geometric engines;
the resulting histogram, exact minimum, budget and containment margin agree
with the completed evidence. Downloading alone is not verification.

The release manifest checks file integrity. It is not a substitute for reading
the mathematical argument or executing the exact geometric checks. Distinct
implementations reduce shared implementation risk; the project does not claim
external human peer review or formal verification.
