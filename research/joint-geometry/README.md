# Global center rules and scoped geometric exclusions for 17 squares

This supplement does **not** prove optimality or improve the accepted global lower bound `s(17)>4.6601`. It records independently checked necessary conditions and local exclusions, plus a clearly separated interrupted research checkpoint. The exact rational feasible cap `4675530093604551/10^15` is not asserted to be the optimum.

## Included evidence

| Folder | Result | Verification status |
|---|---|---|
| `global-area` | Complete 16×16 center grid, 3,026 disk conflicts, all 18,496 rectangle capacities at target 4.67001; an exact 17-cell relaxed survivor | Original Python exact arithmetic and independent Node replay passed; coordinator repeated the checks. Export only rebases paths/hashes and compacts JSON. |
| `local-exclusion` | A geometric contradiction supported on three specified pose boxes, with 2 positive multiplier rows; a coarser affine survivor and feasible-cap row control are retained | Original independent Node replay passed. The compact package includes all 17-box rows used by the checker, although the contradiction uses only labels 9, 11, 13. |
| `historical-summaries` | Completed 61-node coarse-case exclusion and later partial 938-node all-angle forest | Historical receipts only. Full raw traces are preserved locally and are **not** included or independently replayable from these summaries. |
| `pending-round06` | A four-cell disk-secant cut candidate and 16 cap-grid cut candidates, with supports of 3–8 cells | Producer exact arithmetic only. Independent replay did **not** run. The checker is an unrun draft, and the cap-grid master is not exhausted. Do not use these as accepted proof premises. |

The global area rule is necessary for every packing at its stated size; this is not the same as solving the global packing problem. Local exclusions are conditional on exact pose boxes. Every square retains an independent orientation. No charge assumption, individual reflection of a configuration, or localization near the known packing is used by the included geometric certificates.

## Replay the completed evidence

Node.js with built-in modules suffices. Run from each indicated folder:

```sh
cd global-area
node verify_global_localization_test.js
node verify_global_rectangles.js
cd ../local-exclusion
mkdir -p outputs
node verify_linear.js data/three-square-certificate.json outputs/three-square-node.json
node verify_linear.js data/coarser-relaxation-survivor.json outputs/coarser-survivor-node.json
node verify_linear.js data/feasible-cap-row-control.json outputs/cap-control-node.json
```

These commands reconstruct exact rows/capacities and check rational witnesses or contradictions. Original replay receipts are under `receipts/`; their certificate hashes refer to the original pre-export bytes. `PROVENANCE.json` maps those original hashes to the public artifacts and specifies each export adaptation. During publication validation, the portable copies passed both global-area Node checks and all three local-exclusion Node checks. Fresh receipts are in their outputs/ directories. The pending-round06 checker was not run; its candidates remain unverified.

The optional Python discovery scripts use NumPy and SciPy. Discovery is unnecessary to replay frozen certificates. Running a solver again can produce a different witness. Neither a floating solver status nor an affine survivor proves a square packing.

## Limits and retained failures

The disk-only global survivor fails one rectangle capacity, while the stronger model has a different exact survivor. Eight reference index patterns were forbidden only to test whether the relaxation forces those patterns; those artificial test restrictions are not physical packing constraints. The rounded index permutations are not a new whole-container symmetry theorem.

The coarser local certificate has an exact rational affine survivor, showing that this relaxation loses decisive geometry as boxes widen. The accepted feasible construction satisfies the regenerated necessary rows at its own target. The historical three-box cut covered 13×6×1 retained domain choices, but the domain-membership database is omitted here: the compact claim is the explicitly supplied pose-box exclusion, not a fresh replay of the 78-index integration claim.

A complete result still needs exhaustive global center/orientation coverage, independently verified pruning/terminal cases, and a matching exact algebraic feasible endpoint and lower theorem. Strict exclusions at an unrelated rational target cannot establish equality at the optimum.

Research was stopped by the user on 2026-09-29. The interrupted checkpoint is retained for transparency. There are no active jobs or automatic restart instructions in this package.

See `PROOF.md`, `PROVENANCE.json`, and `CHECKSUMS.json`. New geometric code was developed in this project. No external Guzhou or legacy R038 code was executed, imported, compiled, or embedded for these experiments. No S11 theorem is a premise. Existing repository attribution and licensing notices remain applicable and are not superseded by this supplement.
