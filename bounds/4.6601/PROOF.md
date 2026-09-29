# Proof of the intermediate bound s(17) > 4.6601

Let s(17) be the minimum container side for seventeen unit squares with disjoint open interiors. Orientations are independent and touching boundaries are permitted. Set S=46601/10000, L=4613/1000 and A=L/S=46130/46601. A hypothetical unit-square packing at side S rescales to seventeen side-A parents in [0,L]^2.

## Global nonnegative charge budget

The certificate defines a monotone integer charge on captured sites. Its nonnegative weights have scale10^9. A site can lie in at most one disjoint open parent interior. A threshold image with positive site coefficients a_i and threshold k can therefore fire in at most floor(sum(a_i)/k) parents. For a listed family of pairwise-intersecting winning subsets, two disjoint parents cannot both capture winning subsets, so that image has budget one. Point captures have budget one per site. Summing these budgets with the actual integer weights gives M=17000402008. Both mathematical checkers validate the sites, positive coefficients, winning-set intersections, complete D4 orbits and reconstructed budget.

## Every legal center, angle and boundary

Write c(t)=(1-t²)/(1+t²) and s(t)=2t/(1+t²). Each stored rational interval[a,b] has a rational core angle t and side B. Exact support inequalities require

    A > B max_{u in {a,b}} [c(t)c(u)+s(t)s(u)+|c(t)s(u)-s(t)c(u)|].

The validated angular span lies within the region where this support increases with absolute angle difference. The endpoint maximum therefore bounds the whole interval, and the closed core is strictly inside every corresponding side-A parent. The legal-center envelope is[r,L-r]^2, where r=A min_{u in {a,b}}(c(u)+s(u))/2; it includes every legal parent center. The checkers recompute these target-specific inequalities exactly. The 2,543 intervals form a gapless cover from zero to207107/500000, beyond tan(pi/8).

The charge and container are D4 invariant. This reduces a single square's charge minimum to the covered angles; it does not impose a common orientation or independently transform the members of a physical packing.

Integer subset Möbius inversion expresses each capture rule as signed all-subset terms. Their capture regions are rectangles in rotated center coordinates. Exact rational arrangement sweeps bound the charge on every generic cell meeting a conservative cover of the center envelope. Python uses arbitrary-precision rational geometry; the independent Node implementation uses BigInt rational geometry. The absolute sum of signed atom weights is checked below2^50, so the bounded integer sweep accumulations are exact.

Strict containment handles degenerate boundaries: for any legal parent, an arbitrarily small generic perturbation of its core center can remain inside that parent's open interior and within the center envelope. Such a perturbation can avoid all arrangement events, including when the original center lies on an envelope boundary. Every site captured by this perturbed core belongs to the parent's open interior. Monotonicity and nonnegative weights therefore transfer the generic-cell lower bound to the physical parent. Angle endpoints, arrangement boundaries and physical contacts are all covered; a boundary enumeration is not silently assumed.

## Exact contradiction

Complete native, original Python and independent Node verification agree on every one of the2,543 interval minima and cell counts. The achieved uniform bound is Gamma=1000026844, not merely the requested threshold. Therefore any seventeen-parent packing would satisfy both total charge>=17Gamma and total charge<=M, but

    17*1000026844 - 17000402008 = 54340 > 0.

No packing exists at S. The bounded space of centers and square orientations is compact, and containment and interior non-overlap are closed constraints. A minimizing configuration exists, so the exclusion at S yields the strict inequality **s(17)>4.6601**.

Certificate SHA-256: `bed6e09d568a88c0801bcf35d2a1ccab7ca4ce8666601e41de4832f35840daca`. Complete acceptance replay finished2026-09-29T17:12:02.399633+00:00. Exact receipts, checker identities, the positive strict-core margin and every interval result are retained in `evidence/`.

This proves only the displayed intermediate lower bound. A complete determination still requires exhaustive global exclusions up to an identified endpoint and a matching exact feasible construction there.
