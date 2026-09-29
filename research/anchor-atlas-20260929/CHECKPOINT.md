# Checked one-square pose cover; global packing proof unfinished

Research stopped at the user's request on2026-09-29. This checkpoint gives an exhaustive conservative cover of one square's poses over the whole unresolved side interval. It does not enumerate or exclude all seventeen-square configurations, identify the optimum, or improve the accepted4.6601 bound.

Normalize the container to L=4613/1000 and retain A in[L/U,L/(46601/10000)], with U=4675530093604551/10^15. Cover both center coordinates over[0,L] by32 closed intervals and the full modulo-quarter-turn half-angle parameter t over[0,1] by32 closed intervals. Boundary overlaps are retained. There are32,768 indexed boxes. No independent D4 transformations or shared-angle assumption is used.

Exact original Python construction and independent Node checking give:

- 13,336 boxes excluded by conservative wall bounds.
- 19,432 remaining outer pose boxes.
- 3,816 boxes certified to have charge greater than1000023647 throughout their closed domain and the full A interval.
- 15,616 boxes retained as possible low-charge-anchor locations.

High-charge boxes remain available to every non-anchor square. The anchor may or may not be the required tilted square. Both possibilities remain necessary. A center-grid cell has capacity at most one because2(L/32)^2<A_min^2, whereas disjoint squares' inscribed disks require center distance at least A>=A_min. This is a proved capacity bound, not an assumption that repeated cells can always be discarded.

## Why each deletion is sound

On t in[a,b] within[0,1], c(t)=(1-t²)/(1+t²) decreases and s(t)=2t/(1+t²) increases. Their exact endpoint ranges give rational interval bounds. Wall deletions use the safe lower halfwidth A_min(c_min+s_min)/2 and strict separation of a center box from the legal envelope; boundary contact is retained.

For every remaining center/angle box, interval multiplication bounds the two rotated coordinates of each site relative to every possible center. A site is a guaranteed capture only when both absolute-coordinate bounds are strictly below A_min/2. It is then in the open parent interior for every A>=A_min. The exclusion record lists distinct winning feature images supported by such guaranteed sites, with a total integer weight above floor(M/17). Nonnegative omitted charges cannot decrease this lower bound. This direct closed-box argument handles grid, angle and capture-event boundaries without a genericity deletion.

The independent checker reconstructs the accepted source sites/rules, all endpoint bounds, each guaranteed capture and winning witness, the capacity inequality and the complete grid partition. It compares rational values rather than requiring identical unreduced denominators. The initial checker rejected equivalent denominator representations; the corrected replay passed every cell before research stopped.

## Replay and provenance

From the repository root, with Node.js on PATH:

```sh
node research/anchor-atlas-20260929/check_atlas.js research/anchor-atlas-20260929/atlas new-atlas-receipt.json 0 32
```

The accepted charge certificate is supplied by `bounds/4.6601/`. All mathematical angle data are byte-identical to the completed research check. Only a local metadata path, dependent hashes and the checker's path resolution were made portable. `original-verification.json` records the original and portable identities and completion time. Publication replay is bounded verification of the portable copy, not a new research run.

The cover is broad: about80percent of the non-wall boxes remain possible anchor boxes. A Python control against the known feasible construction completed, but its planned independent physical/charge replay was not launched after the shared stop. That unfinished control is not a premise of the atlas claim.

A feasible plan must now combine this cover with sound joint geometry or a different global reduction, retain all unresolved cases and prove the matching exact endpoint. Neither an outer-cover survivor nor pairwise compatibility is a physical packing. No complete joint reduction or optimum is claimed here.
