# Reproduction and exact scope

Run from this contribution's root directory. Python proposal generation requires an existing environment with NumPy and SciPy. The exact replay requires only Node.js and its standard library.

    python source/propose_basis.py
    node source/check_basis.js

The default checker input is `evidence/basis-certificate.json`. The checker reconstructs geometry from `data/upper-packing-certificate.json`, verifies its SHA256 identity, rechecks canonical orientations, all selected rows, full basis rank, exact primal/dual equality and signs, and every physical wall/pair constraint. Its proof decisions use BigInt rational arithmetic only.

The proposer uses floating linear programming only for discovery, followed by exact rational basis reconstruction and an exact simplex repair. A successful numerical exit alone proves nothing. A successful exact replay proves only the recorded selected-separator LP optimum at the fixed rational angles.

The Node checker is byte-for-byte identical to the independently executed checker. For portability, the published certificate's `input_path` is relative. No mathematical certificate field changed. The proposer changes only its input-file assignment and emitted input path. The portable exact certificate was replayed during publication validation; the retained failed proposal was correctly rejected. The discovery scripts were not rerun. [source-provenance.json](source-provenance.json) maps the original tested certificate/checker identities to the portable files and records a common mathematical-payload hash. The original replay receipt intentionally retains the original certificate file hash.

Retained outputs are `basis-certificate.json`, `basis-packing.json`, `exact-pivots.json`, `numerical-proposal.json`, the first failed exact reconstruction, and the original independent replay receipt. The separate symbolic proposal in `proposals/` was never run and has no passing receipt. Its proposed conclusions must not be treated as tested results.
