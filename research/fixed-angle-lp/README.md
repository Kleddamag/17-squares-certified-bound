# S17: exact fixed-angle LP basis checkpoint

This contribution does not determine the minimum enclosing square for 17 independently rotated unit squares. The accepted lower bound remains **s(17)>4.6601**. The known rational feasible enclosure `4675530093604551/10^15` is not asserted to be the exact optimum.

The completed experiment selects one signed separating-axis inequality for each of the 136 pairs, retains all 68 wall inequalities, fixes the construction's exact rational orientations, and minimizes the enclosing side in the resulting 35-variable linear program.

An independent Node BigInt checker passes on a full-rank 35-row basis and its rational primal/dual certificate. It verifies all 204 selected inequalities, nonnegative multipliers, exact force balance and objective equality. It independently rebuilds geometry from vertex projections and verifies all 68 vertices and 136 physical pair separations. The original feasible cap is admitted by the selected LP. The resulting rational side is recorded in [the exact packing](evidence/basis-packing.json).

This certifies the optimum of **one selected-separator LP at one fixed vector of angles**. It does not certify a minimum over separator choices or independently varying orientations. The repaired basis has nine positive multipliers and 26 zeros; its positive support involves only six squares. A requirement that every active basis row carry a positive force would miss this instance.

The first floating basis proposal had an exact selected-row violation of approximately `-7.680192825486122e-61`. [That failed proposal](evidence/failed-basis-proposal-01.json) is retained. One exact simplex pivot repaired it. The numerical solver's optimal status was only a proposal, never the proof decision.

[The reduction draft](PROOF_REDUCTION_DRAFT.md) explains a proposed global route: keep all 17 angles independent, replace translations by a dominating optimal LP vertex, and enumerate its exact angle-dependent basis cases. It includes compact attainment, zero multipliers, degenerate vertices, rattlers, equal angles, endpoints and alternative singular bases. Independent mathematical review of this draft remains pending. Complete basis enumeration/pruning and continuous angle exclusion remain missing; see [the proof gap](PROOF_GAP.md).

[The symbolic core source](proposals/prove_core_formula_unexecuted.py) was **not executed**. No formula or endpoint proposed by it is counted as a completed result. An observed separator graph is not an exhaustive contact classification, and a separator equality need not mean physical contact.

The construction input preserves its existing provenance: a rational reconstruction attributed in its certificate to John Bidwell's 1998 packing. No external source code is included or executed in this contribution.

See [reproduction instructions](REPRODUCE.md), [the original independent replay receipt](evidence/basis-replay-original.json), [source/path provenance](source-provenance.json), and [the manifest](MANIFEST.json).

Publication validation independently replayed the portable certificate and rejected the retained failed basis. See [the publication receipt](evidence/publication-replay.json) and [negative control](evidence/publication-negative-control.json). This validates the same fixed-angle LP scope.
