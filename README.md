# Seventeen unit squares: a certified lower bound

This repository supplies an exact computer-assisted proof that

$$\boxed{s(17)>\frac{466001}{100000}=4.66001.}$$

Here s(17) is the minimum square-container side for seventeen unit squares with pairwise disjoint interiors. Each square may rotate independently; boundary contact is allowed.

The new bound improves the previously released **4.640020** by **0.019990**, closing **56.29%** of that release's remaining gap to the retained Bidwell upper bound **4.675530093604551**. The exact minimum remains unresolved, and no better packing was found.

[Proof](bounds/4.66001/PROOF.md) · [Method](bounds/4.66001/METHOD.md) · [Verification details](bounds/4.66001/README.md) · [Current bound metadata](CURRENT_BOUND.json) · [Attribution](ATTRIBUTION.md)

## What is verified

The fixed rational certificate covers all legal centres and orientations through **2,168 exact orientation intervals** and strictly interior cores. The reconstructed global charge budget is **17,000,402,008**; every core has charge at least **1,000,026,844**, but

$$17\times1000026844=17000456348>17000402008.$$

The surplus is **54,340 integer units**. Original Python rational geometry and the independent JavaScript BigInt implementation agree on every interval minimum and cell count. Sweep accumulators have explicitly checked exact integer bounds.

Certificate SHA-256:

```text
280af3d46150ca990917d714d83ee73baf4e6c45a0563090bf35588fb22de6e5
```

This is a computer-assisted proof, not proof-assistant formalization or independent human peer review. No unqualified world-record or literature-priority claim is made.

## Reproduce the current proof

Use Python 3.12 and Node.js on PATH:

```sh
git clone https://github.com/Kleddamag/17-squares-certified-bound.git
cd 17-squares-certified-bound
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python check_integrity.py
.venv/bin/python bounds/4.66001/verify.py --output-directory .replay-runs/current-proof --workers 1
```

On Windows use `.venv\Scripts\python.exe`. Run without Python `-O`/`-OO` and use a new output directory. `--workers` controls workers per checker; both implementations run concurrently. The replay is local and does not download or execute an upstream checker. Installing dependencies needs network access.

Expected complete result:

```text
status: PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION
target: 466001/100000
budget_units: 17000402008
minimum_units: 1000026844
surplus: 54340
intervals: 2168
```

See the [verification package](bounds/4.66001/README.md) for full receipts, premise/corruption controls and chronology.

## Earlier versions and unchanged packing

The [v1.1.0 instructions](README-v1.1.0.md) and [4.640020 package](bounds/4.640020/README.md) remain intact, as do the [v1.0.0 instructions](README-v1.0.0.md) and original root-level proof. Historical root files `RESULT.json` and `bounds.json` still describe v1.0.0; `CURRENT_BOUND.json` identifies the current theorem. Existing release tags are unchanged.

The retained exact reconstruction of the established Bidwell packing is unchanged. Its separate standard-library check is `python3 verify_upper.py upper-packing-certificate.json`.

## Contributions and reuse

**Kleddamag** directed the research and authorized this GitHub update. **OpenAI Codex** performed the mathematical exploration, implementation, certificate construction and computational verification. The advance combines completed work from separate research tasks and a coordinator's fresh exact replay. See [AUTHORS.md](AUTHORS.md), [ATTRIBUTION.md](ATTRIBUTION.md) and [LICENSING.md](LICENSING.md) for contribution and method lineage.

The unproved 4.67 research and private task conversations are not part of this proof package.
