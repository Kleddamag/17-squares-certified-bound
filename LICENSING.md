# Licence scope

The [MIT licence](LICENSE) applies to this project's original code,
documentation and additions, to the extent copyright or similar rights exist
and the project is entitled to grant them. It does not relicense upstream
material. Attribution remains important even where numerical or mathematical
facts are not subject to copyright.

Third-party notices under `NOTICES/` retain their own terms and are preserved
for attribution and licence compliance. Historical statements in those
verbatim notices describe their original packages, not the current release's
file inventory or theorem. See [ATTRIBUTION.md](ATTRIBUTION.md) for precise
source revisions and the changes made here.

The pinned R038 source tree provides attribution and licence-scope notices,
but no general licence grant for its JavaScript checker was identified.
Consequently this release does not bundle that upstream source or purport to
grant rights in it. `prepare_secondary.py` downloads it at the pinned commit,
checks its SHA-256, applies this project's published edits, and checks the
result against the exact checker used in verification. The cached reconstructed
file remains subject to applicable upstream rights; a local download is not
a new licence grant. An existing pinned source file can be supplied instead.

The original Mira source and certificate are also kept external. This release
contains the new verified rational certificate, its numerical/source lineage,
and preserved source notices.

Joshua Levy's upstream notices distinguish MIT code, CC BY 4.0 documentation
and data, and separately governed third-party works. Both the MIT notice
carried in the pinned R012 lineage and the archived broader licence text are
preserved; neither is represented as a blanket licence for all upstream work.

Python, Node.js, NumPy, Numba and llvmlite are installed dependencies, not
vendored runtime distributions. Their own licences apply to those packages.
