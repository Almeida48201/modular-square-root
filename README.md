# modular_square_root

Computes a square root of an integer modulo an odd prime using Tonelli-Shanks, returning `None` for non-residues.

## Usage

```python
from modular_square_root import modular_sqrt

root = modular_sqrt(5, 11)   # returns 4 because 4*4 ≡ 5 mod 11
print(root)
```

For a prime `p` and integer `a`, `modular_sqrt(a, p)` returns an integer `r` such that `(r * r) % p == a % p`. If `a` is not a quadratic residue modulo `p`, it returns `None`.

## Why this library exists

Finding square roots modulo a prime is a common building block in cryptography and number theory. The Tonelli-Shanks algorithm handles all odd primes, but the simpler formula `pow(a, (p+1)//4, p)` works when `p % 4 == 3`. This library implements both: the fast path for `p ≡ 3 (mod 4)` and the general algorithm for `p ≡ 1 (mod 4)`.

The trade-off is determinism versus speed. A quadratic non-residue is required by Tonelli-Shanks, and many implementations pick one randomly. This library scans small integers starting from 2, which is deterministic and pure, at the cost of a tiny loop. That makes the function easier to test and reason about.

## Edge cases

- `a = 0` always returns `0`.
- Negative `a` is reduced modulo `p` before processing.
- `p = 2` is handled specially and returns `a % 2`.
- Invalid moduli (`p <= 1` or even `p`) raise `ValueError`. The function does not verify primality; passing a composite modulus has unspecified results.

## Exported names

- `modular_sqrt(a, p)` from `modular_square_root.core` (re-exported in `modular_square_root`)
