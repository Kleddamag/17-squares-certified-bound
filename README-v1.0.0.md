# Seventeen unit squares: a certified lower bound

This release supplies an exact computer-assisted proof that

$$
\boxed{s(17)>\frac{461300}{99853}=4.6197910929065726618\ldots.}
$$

Here $s(17)$ is the minimum side length of a square containing seventeen unit
squares with disjoint interiors. Each unit square may rotate independently;
boundary contact is allowed.

**The exact minimum remains unresolved. We have not found a better packing.**
The retained rational reconstruction of the established Bidwell packing gives
the unchanged upper bound $s(17)\le4.675530093604551$. This release makes no
unqualified world-record or literature-priority claim.

[Proof](PROOF.md) · [Verification evidence](VERIFICATION.md) ·
[People and AI contribution](AUTHORS.md) · [Attribution](ATTRIBUTION.md) ·
[Licensing](LICENSING.md) · [Tagged release](https://github.com/Kleddamag/17-squares-certified-bound/releases/tag/v1.0.0)

## What is verified

The fixed rational certificate covers **all centres and orientations**, using
7,853 exact angle intervals and strict interior cores. Its counting inequality
is

$$
17\times1.000020517=17.000348789>16.998427356.
$$

The left side is the required charge for seventeen cores; the right side is
the available total budget. The proof explains why touching parent squares,
event lines, tangencies and domain boundaries are included.

Two exact geometric implementations passed every interval and returned the
same complete histogram of interval minima. The Python checker uses polygon
edge projections; the JavaScript checker adapts Guzhou's R038 clamped-extrema
geometry. Separate automated audits checked all 31,412 containment inequalities,
structural and budget premises, and 3,403 exact boundary/event samples. The
samples supplement the universal proof and full sweep; they are not the
coverage argument. This is a computer-assisted proof, not a proof-assistant
formalization or a claim of external peer review.

Certificate SHA-256:

```text
0288aaac680131aa675adb63ea6a67e3d363fcca6061d4c788301da7c5d69cec
```

## Reproduce the proof

The recorded environment uses Python 3.12.14, NumPy 2.3.5, Numba 0.67.0,
llvmlite 0.49.0 and Node.js 25.6.1. Install Python 3.12 and Node.js, then:

```sh
git clone https://github.com/Kleddamag/17-squares-certified-bound.git
cd 17-squares-certified-bound
git checkout v1.0.0
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python check_integrity.py
.venv/bin/python verify.py --jobs 2 --output .replay-runs/my-verification
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.
Do not use Python's `-O` option. Choose a **new** output directory for each
replay. `--jobs` controls workers per checker; both checkers run concurrently.
Use `--jobs 1` for lower resource use. A replay takes several minutes on the
research machine; other hardware may take longer.

The first run downloads a small, commit-pinned R038 JavaScript source file and
applies this project's published byte edits. It verifies both the source hash
and the reconstructed checker hash before execution. This preserves the exact
previously verified implementation while keeping upstream source under its
own terms. Network access is needed only to prepare that checker and install
dependencies; the certificate scan itself is local. See [licensing](LICENSING.md).

For an existing local copy of the pinned upstream file, prepare without a
download:

```sh
.venv/bin/python prepare_secondary.py --source /path/to/exact_parent_side_scan.js
```

The full replay must finish with:

```text
status: PASS_TWO_COMPLETE_EXACT_REPLAYS
strict_lower_bound: 461300/99853
intervals: 7853
minimum_charge_units: 1000020517
budget_units: 16998427356
counting_surplus_units: 1921433
minimum_containment_margin: 1/1000000000000
histograms_identical: true
```

The independent premise/boundary controls and the existing upper-bound packing
use only Python's standard library:

```sh
python3 independent_controls.py global-certificate.json --output .replay-runs/controls.json
python3 verify_upper.py upper-packing-certificate.json
```

These commands supplement the full replay. The upper checker verifies seventeen
exact unit squares, containment of all 68 vertices and separation of all 136
pairs.

## Release contents

| Files | Purpose |
|---|---|
| `PROOF.md`, `global-certificate.json` | Mathematical argument and fixed rational input |
| `verify.py`, `exact_mixed.py`, `integer_sweep.py`, `replay_*.py` | Complete exact replay |
| `prepare_secondary.py`, `secondary-adaptation.json` | Reconstruct the SHA-pinned secondary checker |
| `independent_controls.py` | Independently implemented containment and boundary controls |
| `evidence/`, `RESULT.json`, `VERIFICATION.md` | Completed results, source identities and release verification |
| `upper-packing-certificate.json`, `verify_upper.py` | Unchanged established packing and exact check |
| `ATTRIBUTION.md`, `AUTHORS.md`, `NOTICES/`, `LICENSING.md` | Contributions, sources and licence boundaries |
| `MANIFEST.json`, `check_integrity.py` | Release file hashes and integrity check |

Unfinished research, numerical search checkpoints and unreplayed candidates
are excluded from this release. The wider research archive remains separate.
The public repository starts with a new history; no existing private repository
was made public.

## Independent verification welcome

Please inspect the proof and checkers, run the complete replay, and report any
issue. An issue with the release tag/commit, runtime versions, certificate hash,
command and output is especially useful. Completed replays and substantive
mathematical objections are both welcome. Solver success or a sample of angles
alone does not verify this theorem.

The project was directed by **Kleddamag**, with substantial research,
implementation and verification work by **OpenAI Codex**. It builds on the
Mira, Guzhou/N17 and Joshua Levy weighted-covering lineage. See the linked
contribution and attribution statements for the precise scope.
