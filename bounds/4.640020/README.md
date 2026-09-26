# Exact certificate for s(17) > 4.640020

This package proves **s(17)>232001/50000**, allowing arbitrary independent
rotations and boundary contact. It does not determine the exact minimum or
improve the known packing.

- [Proof](PROOF.md): global charge budget, continuous coverage and contradiction.
- [Method](METHOD.md): rational cores, envelopes, Boolean rules and exact sweeps.
- [Certificate](certificate.json): fixed rational data, unchanged from the
  completed research audit.
- [Source identities](evidence/theorem-identities.json): unchanged certificate
  and checker hashes.

The certificate's parent side is **A=32950/33143** in the container
**L=4613/1000**, so L/A=232001/50000. Its 2,048 intervals cover a fundamental
orientation sector; the checked D4 symmetry covers the other sectors. The
minimum strict containment margin is **1/100000000000**.

The reconstructed budget is **16,978,369,232**. The certificate requests
coverage of at least **998,727,602** units; complete replay obtains the stronger
minimum **998,727,933**. The latter gives **17 Gamma − M = 5,629 > 0**.
Neither value is a floating-point tolerance.

## Run the complete proof

From the repository root, after installing the root `requirements.txt` in
Python 3.12 and making Node.js available on PATH:

```sh
python bounds/4.640020/verify.py --output-directory .replay-runs/proof-464002 --workers 1
```

Use the Python executable from your environment. The launcher runs both full
implementations, checks exact target identity, requires all 2,048 intervals
from each, compares every minimum and cell count, and requires the strict
counting contradiction. It uses no optimizer, network download or compiled
C++ extension. Python uses NumPy/Numba for bounded integer sweep operations;
geometry is arbitrary-precision rational arithmetic. JavaScript uses BigInt
geometry and integer-valued accumulators with a checked absolute bound below
2^50.

Each checker uses the supplied number of workers, so `--workers 1` runs one
Python worker and one Node process concurrently. Runtime depends on hardware
and other work on the machine; published performance experiments are not a
runtime guarantee for this command. Do not use Python `-O`/`-OO` or set
`PYTHONOPTIMIZE`. Every run needs a new output directory.

Successful completion writes `theorem.json` with status
`PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION`, target `232001/50000`, minimum
`998727933`, budget `16978369232` and surplus `5629`. A failed or partial
process is not a proof.

Additional controls:

```sh
python bounds/4.640020/controls.py --output-directory .replay-runs/controls-464002
```

These exhaust all capture patterns of every distinct active rule, verify
disjoint-capture budgets, compare direct and segment-tree accumulation at
four selected intervals with Node, and reject malformed budgets, coefficients,
symmetry images, angle coverage, non-strict cores, false target metadata and
disjoint winning subsets. They supplement the complete replay; four angles
alone do not establish continuous coverage.

## Evidence and chronology

The original two-implementation verification completed on
**2026-09-25 at 19:39:19 UTC**. The coordinating task independently reran both
complete implementations on copied sources later that day; the completed
comparison was recorded at **19:57:33 UTC**. The release also contains a fresh
publication replay using the portable launcher. Its exact completion time is
recorded in `evidence/publication/theorem.json`.

| Files | Meaning |
|---|---|
| `evidence/r464002-global-python.json`, `r464002-global-js-*.json` | Original complete interval receipts |
| `evidence/r464002-fresh-python.json`, `r464002-fresh-node-*.json` | Coordinator's complete repeated checks |
| `evidence/r464002-retarget-controls.json` | Original target, geometry and corruption controls |
| `evidence/publication/` | Fresh replay through the portable release launcher |
| `evidence/publication-controls.json` | Repeated portable rule and corruption controls |

The launcher was adapted to locate Node on PATH, default to this certificate,
reject optimized Python, and check complete coverage explicitly. The geometric
engines and certificate retain their audited bytes. The two implementations
share the mathematical method; agreement is not a proof-assistant check or
independent human peer review.

Source and method lineage, human direction and Codex's substantive work are
documented in the repository's [attribution](../../ATTRIBUTION.md),
[contributions](../../AUTHORS.md) and [licensing](../../LICENSING.md) files.
