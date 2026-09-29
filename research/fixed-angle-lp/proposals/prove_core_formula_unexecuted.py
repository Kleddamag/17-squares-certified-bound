"""Symbolic verification of the nine-row six-square conditional dual."""
from pathlib import Path
import sympy as sp
import json,datetime,math

root=Path(__file__).resolve().parents[1]
c,s=sp.symbols('c s',nonnegative=True); D=c+s
# Named A,B,C are axis aligned. P,Q,R have the same angle; other 11
# squares are unrestricted and do not occur in this conditional inequality.
xA,yA,xB,yB,xC,yC,xP,yP,xQ,yQ,xR,yR,L=sp.symbols('xA yA xB yB xC yC xP yP xQ yQ xR yR L')
b=(1+c+s)/2
rows=[(yA-sp.Rational(1,2),c/D),
      (L-xB-sp.Rational(1,2),s/D),
      (xC-sp.Rational(1,2),s/D),
      (L-yC-sp.Rational(1,2),c/D),
      (yB-yA-1,c/D),
      (s*(xP-xC)-c*(yP-yC)-b,1/D),
      (s*(xQ-xP)-c*(yQ-yP)-1,1/D),
      (s*(xR-xQ)-c*(yR-yQ)-1,1/D),
      (-s*(xR-xB)+c*(yR-yB)-b,1/D)]
F=(3+3*c+2*s)/D
assert sp.factor(sum(r*w for r,w in rows)-(L-F))==0
# Angular derivative numerator: N'D-ND' = 3(s-c)-1, using c^2+s^2=1.
N=3+3*c+2*s
raw=sp.expand((-3*s+2*c)*D-N*(c-s))
assert sp.expand(raw-(3*(s-c)-1)+(c*c+s*s-1))==0
minimum=(5+sp.sqrt(17))/2
c0=(sp.sqrt(17)-1)/6;s0=(sp.sqrt(17)+1)/6
assert sp.simplify(c0*c0+s0*s0-1)==0
assert sp.simplify(F.subs({c:c0,s:s0})-minimum)==0
# Independent proof of global minimum over c,s>=0, c^2+s^2=1:
# N - minimum*D = 3 + ((1-sqrt17)/2)c - ((1+sqrt17)/2)s.
# The two coefficient magnitudes have norm 3. Cauchy-Schwarz gives >=0.
A=(sp.sqrt(17)-1)/2;B=(sp.sqrt(17)+1)/2
assert sp.simplify(A*A+B*B-9)==0
assert sp.simplify(N-minimum*D-(3-A*c-B*s))==0
count=sum(math.comb(68,35-k)*math.comb(136,k)*8**k for k in range(36))
receipt={'status':'PASS_SYMBOLIC_CONDITIONAL_CORE_DUAL','completion_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'six named squares, three axis aligned and three equal independent-of-container nonnegative-angle representatives, with four selected chain separators plus one vertical separator; not globally exhaustive','formula':'L >= (3+3*cos(theta)+2*sin(theta))/(cos(theta)+sin(theta))','positive_rows':9,'global_angle_minimum_of_formula':'(5+sqrt(17))/2','global_angle_minimum_display':float(minimum),'minimum_angle_cos':'(sqrt(17)-1)/6','minimum_angle_sin':'(sqrt(17)+1)/6','derivative_numerator':'3*(sin(theta)-cos(theta))-1','naive_basis_inventory_upper_bound':str(count),'naive_basis_inventory_decimal_digits':len(str(count)),'endpoint_identified':False}
(root/'evidence/core-formula-symbolic.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('status','global_angle_minimum_display','naive_basis_inventory_decimal_digits')}))
