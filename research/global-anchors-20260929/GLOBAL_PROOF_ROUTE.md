# Necessary anchors for a full S17 proof

These are globally necessary restrictions and an exact counterexample to one localization shortcut. They do not determine s(17). Use the accepted charge in `../../bounds/4.6601/certificate.json`, with M=17000402008, and the known rational feasible cap U=4675530093604551/10^15. U is not asserted optimal.

## A low-charge square must exist

For any seventeen disjoint open square interiors, the accepted nonnegative charge budget gives sum(q_i)<=M. Thus at least one square has integer charge

    q_i <= floor(M/17) = 1000023647,
    M = 17*1000023647 + 9.

More generally q_(k)<=floor(M/(18-k)) for increasingly ordered charges. With G=1000026844 used only as an accounting reference, define d_i=max(G-q_i,0) and h_i=max(q_i-G,0). Then

    sum(d_i)-sum(h_i)=17G-sum(q_i)>=54340.

These consequences do not locate the low-charge square or assert G is a uniform minimum at another side.

## A tilted square must exist

Let phi_i be the distance of square i's orientation from the nearest container axis, in[0,pi/4]. Put delta=2atan(1/28), about4.09degrees. If phi_i<=delta, then cos(phi_i)+sin(phi_i)<=839/785. A unit square with such an orientation contains a concentric axis-aligned square of side B=785/839, whose open interior lies inside the parent's open interior.

If all seventeen squares had phi_i<=delta, their axis-aligned B-cores would have disjoint interiors. Core centers lie in a square of side S-B. Partition each center coordinate into four intervals with consistently assigned endpoints. Because

    S/B <= (839/785)U < 5,
    5-(839/785)U = 2230251465781711/785000000000000000 > 0,

each of the16 center bins has width(S-B)/4<B. Two centers in one bin force overlapping core interiors. Seventeen centers are impossible. Every seventeen-square packing with S<=U therefore has a square with phi_i>delta. The exact arithmetic was independently checked in Python Fraction and Node BigInt; receipts are retained in `evidence/`.

## The anchors can be different

A complete case split must retain both coincident and distinct charge/tilt anchors. Permute identical-square labels to designate them. Apply any D4 normalization to the entire container configuration, not to different squares independently. Each square may still use its intrinsic quarter-turn parameter equivalence. Retain the full unresolved side interval, independent angles, high-charge squares and all boundary cases.

## A corner-only shortcut fails

At L=4613/1000, A=L/U, the exact axis-aligned legal parent with

    x=y=31299014973/10000000000, t=0

has closed-parent charge747604483<=1000023647. Its nearest-wall center distances both equal14830985027/10000000000>A. Thus a low-charge legal square need not be near a corner or even a wall. Closed capture upper-bounds open capture, so the example also has low open charge.

The exact original Fraction calculation and independent Node charge/region receipts are supplied. From this directory, replay with new output filenames:

```sh
node check_parent.js witness-certificate.json witness.json new-witness-check.json
node check_regions.js witness-certificate.json witness.json new-region-check.json
```

The witness is one square, not a seventeen-square packing. It refutes an all-legal-low-squares corner claim, not a hypothetical joint theorem that every seventeen-square packing contains some special corner anchor.

## Still missing

An exhaustive joint case reduction and independently checked exclusions must connect these restrictions to every possible seventeen-body arrangement. Repeatedly excluding selected neighborhoods does not supply global localization. Exact optimality also needs a lower theorem and feasible construction at the same algebraic endpoint. The neighboring `anchor-atlas-20260929` checkpoint constructs a conservative one-square cover only; joint exhaustion remains open.
