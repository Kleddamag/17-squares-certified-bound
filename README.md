# Seventeen unit squares: a certified lower bound

This release supplies an exact computer-assisted proof that

$$
\boxed{s(17)>\frac{232001}{50000}=4.640020.}
$$

Here $s(17)$ is the minimum side length of a square containing seventeen unit
squares with disjoint interiors. Each square may rotate independently, and
boundary contact is allowed.

The previously released bound was **4.619791092906…**. This raises it by
**0.020228907093…**, closing **36.29% of that release's remaining gap**
to the retained Bidwell upper bound of 4.675530093604551.

**The exact minimum remains unresolved. No better packing was found.**
This is a computer-assisted proof, not a proof-assistant formalization or a
claim of independent human peer review. No unqualified public-record or
literature-priority claim is made.

[Proof](bounds/4.640020/PROOF.md) · [Method](bounds/4.640020/METHOD.md) ·
[Verification details](bounds/4.640020/README.md) ·
[Release v1.1.0](https://github.com/Kleddamag/17-squares-certified-bound/releases/tag/v1.1.0) ·
[Human and AI contributions](AUTHORS.md) · [Attribution](ATTRIBUTION.md)

## What is verified

The fixed rational certificate covers **all legal centres and orientations**
through 2,048 exact orientation intervals and strictly interior cores.
Ordinary points, weighted thresholds and pairwise-intersecting subset rules
give a total charge budget of 16,978,369,232 units. Every core has charge at
least 998,727,933 units, but

$$
17\times998727933=16978374861>16978369232.
$$

The exact surplus is **5,629 integer units**. Both complete implementations
agree on every interval minimum and cell count. The geometric engines use
Python arbitrary-precision rationals and JavaScript BigInt respectively;
the sweep accumulators have explicitly checked integer bounds.

Certificate SHA-256:

```text
5f4f0988acc23b738bdf29ee855b9827cda10fce0e12a7b3a78e6923cc5f8dda
```

## Reproduce the current proof

Use Python 3.12 and Node.js on PATH. The recorded Python dependencies are
pinned in `requirements.txt`.

```sh
git clone https://github.com/Kleddamag/17-squares-certified-bound.git
cd 17-squares-certified-bound
git checkout v1.1.0
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python check_integrity.py
.venv/bin/python bounds/4.640020/verify.py --output-directory .replay-runs/current-proof --workers 1
```

On Windows, use `.venv\Scripts\python.exe` instead. Do not use Python's `-O`
option. Choose a new output directory for each replay. `--workers` is the
worker count **per checker**; both implementations run concurrently. The
replay runs locally and does not download or execute an upstream checker.
Installing dependencies requires network access.

Successful output includes:

```text
status: PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION
target: 232001/50000
budget_units: 16978369232
minimum_units: 998727933
surplus: 5629
intervals: 2048
```

The package also includes reproducible rule/budget, direct-sweep and malformed
certificate controls. See [verification details](bounds/4.640020/README.md).

## Earlier release and unchanged packing

The [v1.0.0 instructions](README-v1.0.0.md), original root-level proof,
certificate, checkers and evidence remain available. Those root-level
verification commands still prove **4.619791…**; use the command above for
**4.640020**. The original release tag is unchanged.

The retained rational reconstruction of the established Bidwell packing is
unchanged and can be checked with:

```sh
python3 verify_upper.py upper-packing-certificate.json
```

## Contributions and reuse

**Kleddamag** directed the project and chose to publish this milestone.
**OpenAI Codex** performed the mathematical exploration, implementation,
certificate construction and computational verification. The advance combines
completed findings from separate Codex research tasks. See [AUTHORS.md](AUTHORS.md)
for the division of work and [ATTRIBUTION.md](ATTRIBUTION.md) for the Mira,
Guzhou/N17 and Joshua Levy method lineage.

Download the proof and code, replay the checks, and build on the result.
Unfinished 4.65 research and unverified candidates are not included.
