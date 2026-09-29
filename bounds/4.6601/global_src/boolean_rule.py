"""Exact multilinear expansion of a weighted finite-set threshold predicate."""
from functools import lru_cache
@lru_cache(None)
def expansion(coefficients,k,winning_masks=()):
 n=len(coefficients);values=[int(any(mask&w==w for w in winning_masks)) if winning_masks else int(sum(coefficients[j] for j in range(n) if mask>>j&1)>=k) for mask in range(1<<n)]
 # Subset Mobius transform, performed entirely with integers.
 for j in range(n):
  for mask in range(1<<n):
   if mask>>j&1:values[mask]-=values[mask^(1<<j)]
 return tuple((tuple(i for i in range(n) if mask>>i&1),a) for mask,a in enumerate(values) if a)

def check(coefficients,k):
 terms=expansion(tuple(coefficients),k);n=len(coefficients)
 for mask in range(1<<n):
  actual=sum(a for subset,a in terms if all(mask>>i&1 for i in subset));expected=int(sum(coefficients[j] for j in range(n) if mask>>j&1)>=k)
  assert actual==expected
 return {'coefficients':coefficients,'threshold':k,'terms':terms,'budget':sum(coefficients)//k,'absolute_sum':sum(abs(a) for _,a in terms)}
if __name__=='__main__':
 import json
 print(json.dumps(check([2,1,1,1],3),indent=2))
