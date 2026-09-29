# Research checkpoint: September 29, 2026

The certified theorem is **s(17) > 4.6601**; see [the complete proof package](../bounds/4.6601/README.md). This collection records work toward a complete determination. It does not establish optimality.

| Contribution | Completed evidence | Remaining limitation |
| --- | --- | --- |
| [Global anchors](global-anchors-20260929/GLOBAL_PROOF_ROUTE.md) | Every packing below the feasible cap has a low-charge square and a tilted square. An exact interior witness rules out a proposed single-square corner shortcut. | The two anchors may differ; no complete localization follows. |
| [Pose atlas](anchor-atlas-20260929/CHECKPOINT.md) | Exhaustive conservative cover of 32,768 one-square pose boxes over the unresolved side interval; 15,616 possible low-anchor boxes remain. | No joint seventeen-square exhaustion. Non-anchor squares retain high-charge boxes. |
| [Joint geometry](joint-geometry/README.md) | Exact center-grid/area rules, retained relaxed survivors and a specific pose-box exclusion; publication replays passed. | Historical forests are summaries only. New disk-secant cuts are pending independent verification. |
| [Fixed-angle LP](fixed-angle-lp/README.md) | Exact primal/dual optimum of one 35-variable selected-separator LP, with all 68 vertices and 136 physical pairs checked. | Angles and separator choices are fixed. The proposed global reduction is an unreviewed draft. |

These approaches address different missing steps. A useful full proof must cover every physical arrangement, including independent rotations, degeneracies and boundaries, and establish a lower theorem at the same exact endpoint as a feasible construction. Local exclusions and successful finite experiments do not supply that global coverage.

The known feasible rational enclosure is 4.675530093604551. It is a valid upper bound, not an asserted algebraic optimum. No competing result or priority claim is made here.

The snapshot includes retained failed proposals and explicitly unexecuted work so future investigations can reproduce what was checked and avoid treating proposals as premises. [Publication validation](../PUBLICATION_VALIDATION.json) distinguishes fresh portable checks from reused complete verification.
