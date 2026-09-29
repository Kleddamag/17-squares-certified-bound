# Seventeen unit squares: a certified lower bound

This repository contains a reproducible computer-assisted proof that

$$\boxed{s(17)>\frac{46601}{10000}=4.6601.}$$

Here $s(17)$ is the smallest side length of a square containing seventeen unit
squares with disjoint interiors. Each square may rotate independently, and
boundary contact is allowed. The retained Bidwell construction gives the upper
bound **4.675530093604551**. This project has not proved the exact optimum or
found a better packing.

[Proof](bounds/4.6601/PROOF.md) · [Verification](bounds/4.6601/README.md) ·
[Current bound](CURRENT_BOUND.json) · [Research notes](research/README.md) ·
[Attribution](ATTRIBUTION.md)

## The certified result

The fixed rational certificate covers every legal center and orientation with
**2,543 exact orientation intervals** and strictly interior cores. The global
charge budget is **17,000,402,008** integer units. Every core receives at least
**1,000,026,844** units, but

$$17\times1000026844=17000456348>17000402008.$$

The strict surplus is **54,340**. Complete Python and independently implemented
JavaScript BigInt checks agree on every interval minimum and cell count. The
4.6601 certificate refines the geometry for the new target while retaining the
accepted charges; minima from a different target are not assumed to transfer.

Certificate SHA-256:

```text
bed6e09d568a88c0801bcf35d2a1ccab7ca4ce8666601e41de4832f35840daca
```

This is a computer-assisted proof, not proof-assistant formalization or external
human peer review. The supporting mathematics, fixed inputs and exact checks
are included for independent reproduction.

## Reproduce the proof

Use Python 3.12 and Node.js:

```sh
git clone https://github.com/Kleddamag/17-squares-certified-bound.git
cd 17-squares-certified-bound
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python check_integrity.py
.venv/bin/python bounds/4.6601/verify.py --output-directory .replay-runs/current-proof --workers 1
```

On Windows use `.venv\Scripts\python.exe`. Run without Python `-O`, `-OO` or
`PYTHONOPTIMIZE`, and use a new output directory. The current proof path runs
locally without downloading an upstream checker. Dependency installation
requires network access.

The complete result must report target `46601/10000`, 2,543 intervals, minimum
`1000026844`, budget `17000402008` and surplus `54340`. See the
[verification instructions](bounds/4.6601/README.md) for the exact commands,
receipts and reuse of previously completed checks.

The unchanged upper construction has a separate standard-library check:

```sh
python3 verify_upper.py upper-packing-certificate.json
```

## Research checkpoint

Research stopped on September 29, 2026. The [research notes](research/README.md)
preserve globally necessary restrictions, conditional exclusions, completed
experiments and unfinished proof routes. They do **not** establish optimality.
Their individual proof and verification scopes are stated separately from the
certified lower bound above.

The main missing steps are a complete reduction covering every possible
arrangement and a lower theorem matching a feasible construction at the same
exact endpoint. Excluding selected configurations does not supply those steps.

## Earlier results and contributions

The [4.66001 package](bounds/4.66001/README.md),
[4.640020 package](bounds/4.640020/README.md), and
[original release](README-v1.0.0.md) remain available. The original root-level
`PROOF.md`, `RESULT.json` and `bounds.json` are historical; `CURRENT_BOUND.json`
identifies the current theorem. Existing release tags are preserved.

**Kleddamag** directed the research and maintains the repository. **OpenAI Codex**
performed mathematical exploration, implementation, certificate construction,
computational verification and documentation. See [Contributions](AUTHORS.md),
[Attribution](ATTRIBUTION.md) and [Licensing](LICENSING.md) for roles and source
lineage. Corrections and independent reproduction are welcome through
[GitHub issues](https://github.com/Kleddamag/17-squares-certified-bound/issues).
