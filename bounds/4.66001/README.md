# Exact certificate for s(17) > 4.66001

This package proves **s(17)>466001/100000**, with arbitrary independent rotations and boundary contact. The exact minimum remains open.

- [Proof](PROOF.md): strict cores, continuous coverage and the counting contradiction.
- [Method](METHOD.md): exact geometry, global charge budgets and arithmetic bounds.
- [Certificate](certificate.json) and [identities](evidence/theorem-identities.json).

The parent side is A=461300/466001 in the container L=4613/1000. The certificate contains 2,168 consecutive orientation intervals. Its recomputed minimum support-containment margin exceeds 1/10000000000; the exact rational value is in `evidence/publication-controls.json`. Eight of the original 2,048 intervals were subdivided into sixteen each with regenerated strict cores; the charge stayed fixed. The checkers validate the actual interval chain and geometry.

The reconstructed budget is **M=17,000,402,008**. The certificate requests **1,000,023,648** charge units, already a strict surplus of 8. Full replay obtains **Gamma=1,000,026,844**, giving **17 Gamma − M = 54,340 > 0**. These are exact integers.

## Reproduce

From the repository root, with the pinned Python requirements and Node.js on PATH:

```sh
python bounds/4.66001/verify.py --output-directory .replay-runs/proof-466001 --workers 1
python bounds/4.66001/controls.py --output-directory .replay-runs/controls-466001
```

Use the Python executable from your environment, without `-O`/`-OO` or `PYTHONOPTIMIZE`. Each run needs a new output directory. The launcher runs one Python worker and one Node process concurrently by default. It uses this project's preserved general-rule checkers, no optimizer, external source download or compiled C++ checker.

The complete replay must produce `PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION`, target `466001/100000`, 2,168 intervals, budget `17000402008`, minimum `1000026844`, and surplus `54340`. Both implementations must cover every interval and agree on every minimum and cell count. A successful subprocess or a sampled scan is insufficient. Controls separately exhaust each active Boolean rule, check disjoint-capture budgets, compare direct and segment-tree sweeps at four intervals, and reject malformed certificates.

## Evidence and provenance

The first full research verification completed on September 26, 2026 at 15:37:09 UTC. Both complete implementations were replayed again, finishing at 15:42:25 UTC. Full interval receipts and a public summary are retained in `evidence/coordinator-replay/`. `evidence/publication/` contains the fresh replay of this portable package; `evidence/publication-controls.json` contains its additional controls.

The certificate and mathematical engines retain their audited bytes. The public launcher changes only its default target and expected interval count from the earlier package; the controls change target identity and sampled interval indices. The certificate's `source` text records an earlier construction stage and says the diagnostic was pending; it is preserved to retain the certificate hash. The later completed receipts establish verification.

The certificate combines two charge candidates; subsequent subdivision closes the remaining exact coverage gap without changing charge. Numerical search explains how the certificate was found and is not a proof premise. The two checkers implement the same mathematical argument; this is a computer-assisted proof, not proof-assistant formalization or independent human peer review. [Attribution](../../ATTRIBUTION.md), [contributions](../../AUTHORS.md) and [licensing](../../LICENSING.md) describe the lineage and scope.
