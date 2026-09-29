# Exact certificate for s(17) > 4.6601

This package proves **s(17) > 46601/10000 = 4.6601** for seventeen unit squares with arbitrary independent rotations and boundary contact. This package does not determine the exact optimum.

The certificate has 2,543 consecutive angle intervals, container side L=4613/1000 and parent side A=46130/46601. Its nonnegative integer charge has global budget M=17,000,402,008. Complete checking achieves Gamma=1,000,026,844, so **17 Gamma − M = 54,340 > 0**. The requested threshold, 1,000,023,648, is distinct from the achieved minimum.

Certificate SHA-256:

    bed6e09d568a88c0801bcf35d2a1ccab7ca4ce8666601e41de4832f35840daca

Read [PROOF.md](PROOF.md) for the mathematical argument and [evidence/accepted-review.json](evidence/accepted-review.json) for identities and accepted verification scope.

## Reproduce

Use Python 3.12 and Node.js 18 or newer, with Node on PATH. Install the pinned dependencies into your own environment if needed:

```sh
python -m pip install -r bounds/4.6601/requirements.txt
python bounds/4.6601/verify.py --output-directory .replay-runs/proof-46601 --workers 1
```

Run from the repository root. Use a new output directory for each replay. Do not use Python `-O`, `-OO` or `PYTHONOPTIMIZE`. The launcher invokes the preserved original Python mathematical engine and independent Node checker, validates all geometry/rules/budgets, and compares every interval minimum and cell count. It requires `PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION`, target `46601/10000`, 2,543 intervals, achieved minimum `1000026844`, budget `17000402008`, and surplus `54340`. One successful process, sampled intervals or a requested threshold is insufficient.

The package needs no optimizer, native C++ extension, external source download or legacy reconstructed checker. The original mathematical checker files and certificate retain their accepted bytes. The portable launcher changes the previous public package's default target and expected interval count only.

## Evidence and limitations

Native verification completed on September 29, 2026 at 17:01:54 UTC. Original Python and independent Node checking completed by 17:04:33 UTC. A separate complete Python/Node acceptance replay finished at **17:12:02 UTC**. Its complete interval receipts and the original native receipt are included under `evidence/`; they agree on all 2,543 minima and cell counts. Publication packaging reuses these unchanged complete checks. Any bounded portable smoke check is labeled separately and is not described as another full replay.

This is an exact computer-assisted proof, not proof-assistant formalization or independent human peer review. Numerical optimization helped discover the charges but is not a proof premise. The accepted upper construction is not asserted to be the exact optimum. The repository's existing [attribution](../../ATTRIBUTION.md), [contribution statement](../../AUTHORS.md) and [licensing scope](../../LICENSING.md) remain applicable. This package contains the project's own general-rule checkers; it does not execute or bundle the legacy reconstructed source path.
