# Exact charging argument and its limits

This released target is T = 232001/50000 = 4.640020, container side L = 4613/1000, and parent side A = L/T = 32950/33143. A packing of seventeen unit squares in a square of side T rescales to seventeen A-squares in the L-container. All orientations and legal centres must be covered; a finite placement fit is insufficient.

For a rational half-angle interval [a,b], let t=(a+b)/2. Write c(u)=(1-u²)/(1+u²) and s(u)=2u/(1+u²). The certificate's concentric core has orientation t and side

    B = (A - 10^-11) / max_{u in {a,b}} (c(t)c(u)+s(t)s(u)+|c(t)s(u)-s(t)c(u)|).

The angular intervals are short and the exact check verifies the relevant positive-dot-product range. The endpoint maximum bounds the support over the whole interval. Hence the core lies strictly inside every corresponding parent. The conservative centre envelope is [r,L-r]², where r=A min_{u in {a,b}}(c(u)+s(u))/2. The exact validator recomputes these inequalities. The 2,048 contiguous intervals begin at zero and end at 207107/500000 > sqrt(2)-1. D4 invariance supplies every remaining square orientation.

There are three types of nonnegative charge features, each summed over a complete D4 orbit.

1. A point capture has budget one per physical point.
2. A weighted threshold on distinct sites with positive integer coefficients a_i fires when the captured coefficient sum reaches k. Disjoint strict cores can consume each site's coefficient at most once. Therefore at most floor(sum_i a_i/k) cores fire that feature image. Ordinary k-of-n thresholds are the special case a_i=1.
3. An intersecting-rule feature fires when the captured sites contain at least one listed winning subset. Every two listed winning subsets must intersect. Two disjoint strict cores cannot both contain winning subsets, so the budget is one per image. Fano triple rules and the numerically proposed general intersecting rules are both instances; the checker tests the actual subsets, not a family name or an optimizer's assertion.

Integer weights are rounded upward at scale 10^9. Rounding is not assumed to preserve any numerical guarantee: each exact certificate is audited again. The budget M is reconstructed from its actual integer weights, sites, coefficient rules, winning subsets and symmetry images. Duplicate images, if coalesced, carry their exact multiplicity in the weight.

Each monotone Boolean capture rule is expanded by integer subset Möbius inversion into signed all-subset-capture terms. An all-subset capture is a rectangle in rotated centre coordinates. Python uses arbitrary-precision rational geometry; JavaScript independently uses BigInt rational geometry. Each implementation sorts every rectangle endpoint exactly, sweeps the arrangement, and obtains the minimum integer charge on a conservative cover of the entire centre domain. Signed accumulations are bounded by the sum of absolute atom weights, checked below 2^50; Python int64 and JavaScript exact integers therefore suffice for the sweep sums. The original capture rules are monotone: on arrangement boundaries, additional closed captures cannot lower the charge. Interior-cell lower bounds consequently cover boundaries too.

The paired audit must cover all 2,048 intervals, match the certificate identity, and agree on every interval minimum and cell count. Additional controls exhaust each active Boolean rule, compute its maximum disjoint-winning-set count, compare direct-array and segment-tree sweeps, compare selected Python/JavaScript intervals, and reject corrupted budgets, coefficients, symmetry orbits, angular coverage, core strictness and disjoint winning subsets.

Let Gamma be the resulting universal strict-core charge. Seventeen packed parents would imply 17 Gamma <= M. Only a verified strict reverse inequality excludes the packing. A ratio M/Gamma greater than or equal to 17 is a universal charge guarantee, not a side-bound theorem. If exclusion at T is proved, compactness of bounded centres and orientations, together with closed non-overlap conditions, yields s(17)>T.

Exact actual-parent probes are separately checked using the certificate's integer charge, rational pose and full parent side A. A probe with 17F<M obstructs that fixed charge regardless of orientation refinement. It does not obstruct reweighting, changed sites, other feature families or other packing arguments.
