# Mathematical implications and exact scope

## Center grid, disk conflicts and area capacities

For target `S=467001/100000`, use container `L=4613/1000` and square side `A=L/S`. Every square contains an open disk of radius `A/2`; hence distinct centers in an interior-disjoint packing have distance at least `A`, and all centers lie in `[A/2,L-A/2]^2`. The saved closed center grid covers this square, including boundary cases. Assign a shared-boundary center to any containing cell. Each cell has diameter strictly below `A`, so it has capacity one. If the maximum possible center distance between two cells is below `A`, they cannot both be occupied. The checker rebuilds all 32,640 unordered comparisons and all 3,026 conflicts.

Put `r=707107/10^6`. Since `2r²>=1`, `H=rA>=A/sqrt(2)`. Every coordinate half-width of every rotated side-A square is at most H. If a square's center lies in window `[x0,x1]×[y0,y1]`, the square lies in

`[max(0,x0-H),min(L,x1+H)] × [max(0,y0-H),min(L,y1+H)]`.

If k interior-disjoint squares have centers there, their total area is `k A²`, at most this rectangle's area. Therefore its occupancy is at most the floor of that area divided by `A²`. Closed boundaries cause no area problem. The checker reconstructs all 18,496 grid windows, all exact floors, and the retained relaxed witness. No angle or charge class is removed.

These inequalities constrain every physical packing. Their surviving integer cell assignment supplies no physical square orientations or centers and is not a square packing. It disproves only the sufficiency of these particular relaxation rules for the tested classification.

## Local separating-axis certificate

For each independent half-angle parameter t use

`u(t)=((1-t²)/(1+t²),2t/(1+t²))`, `v(t)=(-u_y,u_x)`.

Every supplied t interval lies in `[-1/2,1/2]`. Rational interval arithmetic encloses both axes. Interior-disjoint side-A squares admit at least one signed separating axis n among the two axes of either square, with

`n·(p_j-p_i) >= A/2 (1+|n·u_other|+|n·v_other|)`.

Retain an alternative unless its projection upper bound is strictly below a lower bound r on the right side. For any fixed rational vector m and any retained alternative, an interval lower bound e on `(m-n)·(p_j-p_i)` implies `m·(p_j-p_i)>=r+e`. Taking the minimum over every retained alternative gives a necessary affine inequality. Thus the construction preserves the separating disjunction rather than choosing an unproved separator. The checker reconstructs all these rows directly from the exact pose boxes.

Write the rows as `BX<=b`, where X consists of all center coordinates within the supplied boxes. If `lambda>=0`, every solution would satisfy `lambda BX<=lambda b`. Compute the exact minimum of the linear form `lambda BX` over the coordinate box by selecting the appropriate endpoint for each coefficient. A strictly positive difference `min_box(lambda BX)-lambda b` is a contradiction. Floating optimization proposes multipliers only; it is not the proof check.

The included three-square certificate has two positive multiplier rows, involving zero-based labels 9, 11 and 13. All other labels have zero coefficients in these rows. Consequently simultaneous occupancy of those three specified pose boxes is impossible, irrespective of any other squares. The exact surplus and boxes are in `local-exclusion/data/three-square-certificate.json` and its support summary. This is a conditional local theorem and does not force a packing into those boxes.

## Interrupted cap-wide secant experiment — not accepted evidence

For unit squares with side S no greater than the rational feasible cap U, retain the packing inside `[0,U]^2`. Its centers lie in `[1/2,U-1/2]^2`; the proposed uniform 16×16 grid covers that entire interval. No artificial reference-template exclusions were used in this master.

Within a pair of selected cells, let a displacement coordinate d lie in `[l,u]`. The elementary inequality `(d-l)(d-u)<=0` gives

`d² <= (l+u)d-lu`.

Apply it to both coordinates and use the necessary disk condition `dx²+dy²>=1`. This yields a necessary affine inequality using the SAME center variables for every incident pair. A positive exact Farkas surplus on a subset would imply an occupancy cut forbidding simultaneous use of that subset of cells.

The producer saved one four-cell candidate for the preceding survivor and 16 candidates in the cap-wide model. Python rational arithmetic checked their proposed contradictions, but the independent checker launch was blocked by the research stop. Both the implementation coverage and the independent replay remain pending. The elementary derivation does not by itself validate an unrun implementation, and the finite assignment master has no exhaustion certificate. The pending files are research provenance only.

## Missing global and endpoint arguments

All cuts require their original target, cell/pose domains and exact source identities. A complete proof needs a gapless map from every physical packing to terminal cases, exact pruning or feasibility at every case, and a verified endpoint. Terminal classes containing a feasible optimum require inequalities valid at equality, not an endless sequence of strict rational-target contradictions. The known rational cap is a feasible bound, not an identified exact optimum. None of this supplement closes that gap.
