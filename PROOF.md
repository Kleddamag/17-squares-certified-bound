# A verified lower bound for seventeen unit squares

For seventeen arbitrarily oriented unit squares with disjoint interiors, allowing boundary contact,

$$
\boxed{s(17)>\frac{461300}{99853}=4.6197910929065726618\ldots.}
$$

This exact computer-assisted proof improves the preserved bound 461300/99951. It does not resolve the exact minimum, improve the packing, or assert literature priority. The discovery optimizer is not a proof premise.

## Exact certificate

The container side is L=4613/1000 and the hypothetical parent-square side is A=99853/100000. Coordinates have denominator 10^8; weights have denominator 10^9. The source of truth is `global-certificate.json`, SHA-256

`0288aaac680131aa675adb63ea6a67e3d363fcca6061d4c788301da7c5d69cec`.

The certificate contains 1,134 distinct point orbits under the eight square symmetries, expanding to 8,988 sites. Point weights are positive on 852 orbits, or 6,744 sites. There are 253 positive two-of-three orbits, expanding to 2,008 physical triples of distinct sites. Sites needed only by a triple can have zero ordinary point weight.

| Quantity | Exact value |
|---|---:|
| Ordinary point budget | 14.640116080 |
| Two-of-three budget | 2.358311276 |
| Total budget M | 16.998427356 |
| Minimum core charge Γ | 1.000020517 |
| 17Γ | 17.000348789 |
| 17Γ − M | 0.001921433 |
| Angle intervals | 7,853 |
| Minimum strict containment margin | 10^−12 |

## Counting inequality

An ordinary site p with weight w≥0 charges a closed square Q the amount w if p∈Q. Across pairwise disjoint closed squares this site's total charge is at most w.

A triple of distinct sites with weight w≥0 charges Q the amount w if Q contains at least two sites of the triple. Two disjoint closed squares cannot both qualify, since any two two-element subsets of a three-element set intersect. This triple's total charge is also at most w. Different triples may share sites: independently valid inequalities can still be added.

Let C(Q) be the sum of all these charges. For pairwise disjoint closed cores Q₁,…,Q₁₇,

$$
\sum_{i=1}^{17}C(Q_i)\le M=16.998427356.
$$

It remains to show that every legal parent square of side A contains a strict interior core with charge at least Γ. The following finite exact verification covers the continuous space of all parent positions and orientations.

## Covering all orientations with strict cores

For rational half-angle t define

$$
c(t)=\frac{1-t^2}{1+t^2},\qquad s(t)=\frac{2t}{1+t^2}.
$$

A catalogue row (a,b,t,B) assigns a concentric closed core of side B and orientation 2 arctan(t) to every parent with half-angle u∈[a,b]. The intervals join exactly from zero to beyond √2−1. Invariance of the charge under the eight container symmetries allows any individual parent orientation to be folded into [0,π/4]. This makes no symmetry assumption about a packing.

Write

$$
F=\max_{u\in\{a,b\}}\bigl(c(t)c(u)+s(t)s(u)+|c(t)s(u)-s(t)c(u)|\bigr).
$$

The verifier checks that the relative angles throughout each interval lie in [−π/4,π/4]. On this range cos δ+|sin δ| increases with |δ|, so its maximum is at an interval endpoint. It checks A−BF>0 exactly for every row. Thus each closed core lies strictly inside every corresponding parent. The minimum checked margin is 10^−12. Stored B values need not come from the final A: their strict containment is checked afresh at that final value.

The legal parent centres at half-angle u form the square

$$
[A(c(u)+s(u))/2,\ L-A(c(u)+s(u))/2]^2.
$$

The function c(u)+s(u) has no interior minimum on the relevant range. Consequently the union of legal-centre domains for u∈[a,b] is contained in, and in fact equals, [r,L−r]², where

$$
r=\frac A2\min\{c(a)+s(a),c(b)+s(b)\}.
$$

Both scanners cover this entire centre domain. A separate independent audit avoids the endpoint argument for containment: it checks the minima of four rational quadratic polynomials over every interval, including any interior critical point. All 31,412 inequalities passed.

## Exact scanning of all centres

For fixed B,t, express centres and sites in axes parallel to the core edges. A site p is captured precisely on a closed rectangle of centres, with half-width B/2 in both axes. For Boolean capture indicators i,j,k,

$$
\mathbf1_{i+j+k\ge2}=ij+ik+jk-2ijk.
$$

Every pair or triple intersection of capture rectangles is another rectangle, possibly empty or degenerate. Thus C equals a signed integer weighted rectangle sum on every generic centre. All geometry is rational and is compared using unbounded integer arithmetic after clearing denominators.

Rectangle edges partition the centre domain into constant-charge open cells. The Python implementation computes the rotated legal-centre polygon's exact edge projections in each vertical slab. Its interval queries include every cell intersecting the polygon. The separately implemented JavaScript checker uses clamped-extrema formulas adapted from the Guzhou scanner. It uses BigInt for all geometric comparisons. The implementations have different slab partitions.

Each accumulator is bounded in absolute value by the sum of point weights plus five times the sum of triple weights. The certificate's bound is below 2^50. Thus signed 64-bit accumulation in Python/Numba and integer-valued Number accumulation in JavaScript are exact; no floating geometric tolerance enters a pass/fail decision.

Both complete replays passed for the pinned certificate, independently giving minimum charge 1,000,020,517 integer units. Their complete histograms of the 7,853 interval minima agree. The Python partition used 124,557,987 relevant slabs and represented 1,641,130,192,125 reachable open cells through range-minimum queries. The JavaScript partition used 124,542,281 slabs. The cells are certified by the sweep, not individually enumerated.

## Event lines, tangencies and domain boundaries

The signed rectangle expansion is not a positivity argument. Boundary coverage follows instead from the original logical charge. Each site's capture set is closed; each triple's qualifying set is a finite union of closed pair-capture sets. Their indicators are upper semicontinuous, and all logical weights are nonnegative.

Every point of the closed centre domain is a limit of generic points in its positive-area interior. If all generic charges are at least Γ, upper semicontinuity implies that the charge at their limit is also at least Γ. Hence omission of degenerate rectangles from the open-cell sweep does not omit a possible low-charge boundary centre. An independent control additionally evaluated 3,403 exact boundary/event centres directly from logical membership. These samples are controls; the universal boundary conclusion is the preceding argument.

## Contradiction and strict inequality

Suppose seventeen side-A parents fit in the side-L container with disjoint interiors. Select the strict closed core prescribed for each parent's orientation. These cores are pairwise disjoint, even when parent boundaries touch. Their charges therefore obey both

$$
\sum_i C(Q_i)\ge17\Gamma=17.000348789
\quad\text{and}\quad
\sum_i C(Q_i)\le M=16.998427356,
$$

a contradiction. Scaling excludes seventeen unit squares in a container of side L/A=461300/99853.

The minimum container side is attained. Restricting to sides below any known feasible upper bound puts centres, orientations and side length in a compact parameter space. Containment and non-overlap of interiors are closed conditions. In particular, a limit of feasible packings is feasible; an interior intersection in the limit would persist under sufficiently small perturbations. Exclusion at L/A therefore gives the strict lower bound stated at the start.

The retained rational construction proves the unchanged upper bound

$$
s(17)\le\frac{4675530093604551}{10^{15}}=4.675530093604551.
$$

## Verification and provenance

Run `verify.py` as described in `README.md` for two fresh complete replays. The secondary checker is reconstructed from pinned upstream bytes plus the published adaptation and is required to match the previously verified checker SHA-256 exactly. `independent_controls.py` separately checks universal strict containment and selected logical boundary values. Original full logs/results and independent structural audits are in `evidence/`. The package launcher was also tested with two fresh complete replays from the portable files.

This is a computer-assisted proof, not a proof-assistant formalization. It depends on the supplied checker implementations and their runtimes. The numerical search, weight averaging, and adaptive builder are discovery tools; the final proof depends only on the fixed rational certificate and the exact verification above. Exploratory finite experiments and unreplayed research candidates are excluded from this verified release.

The work continues the weighted-covering and strict-core method in the audited Mira/Guzhou R038 lineage. The earlier certificate's public source pins and attribution/licence-scope notes are preserved under `NOTICES/` and in `ATTRIBUTION.md`; the prior bound's local artifact remains unchanged. No claim of independent invention of that established method is made.
