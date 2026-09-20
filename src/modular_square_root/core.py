"""Core implementation of the Tonelli-Shanks algorithm.

The algorithm computes square roots modulo an odd prime.  It is
non-deterministic because it needs a quadratic non-residue; we
select one deterministically by scanning small integers in order.
This avoids any dependency on randomness and keeps the function
pure, which makes testing straightforward.
"""

from __future__ import annotations


def _is_quadratic_residue(a: int, p: int) -> bool:
    """Return True when *a* is a quadratic residue modulo prime *p*.

    Euler's criterion is used because it is simple and sufficient for
    prime moduli.
    """
    return pow(a, (p - 1) // 2, p) == 1


def _find_non_residue(p: int) -> int:
    """Return a quadratic non-residue modulo prime *p*.

    We scan from 2 upwards.  This is deterministic and bounded: for an
    odd prime at least one of 2, 3, 4, ... is a non-residue, and in
    practice the first few values are sufficient.  The scan is safe
    because every integer not divisible by *p* is either a residue or a
    non-residue.
    """
    z = 2
    while _is_quadratic_residue(z, p):
        z += 1
    return z


def modular_sqrt(a: int, p: int) -> int | None:
    """Return a square root of *a* modulo prime *p*, or None.

    The returned root *r* satisfies ``(r * r) % p == a % p``.  When
    *a* is not a quadratic residue modulo *p*, None is returned.

    Parameters
    ----------
    a:
        The integer whose square root is desired.  Negative values are
        accepted and are interpreted modulo *p*.
    p:
        An odd prime modulus.  The function does not verify primality;
        the caller must supply a prime.  The behaviour for composite
        moduli is unspecified and should not be relied upon.

    Returns
    -------
    int or None
        A square root in the range ``0 <= r < p``, or None when no
        square root exists.

    Notes
    -----
    The Tonelli-Shanks algorithm is used for primes of the form
    ``p % 4 == 1``.  For ``p % 4 == 3`` the simple closed form
    ``pow(a, (p + 1) // 4, p)`` is faster and is handled separately.
    """
    if p == 2:
        # The only even prime.  Every element is a quadratic residue
        # and the unique square root of a is a % 2.
        return a % 2

    if p <= 1 or p % 2 == 0:
        raise ValueError("modulus must be an odd prime")

    a %= p

    if a == 0:
        return 0

    if not _is_quadratic_residue(a, p):
        return None

    # Simple case: p ≡ 3 (mod 4)
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Tonelli-Shanks for p ≡ 1 (mod 4)
    # Write p - 1 = q * 2^s with q odd.
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    z = _find_non_residue(p)
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)

    while t != 1:
        # Find least i, 0 < i < m, such that t^(2^i) == 1
        i = 0
        temp = t
        while temp != 1:
            temp = (temp * temp) % p
            i += 1
            if i == m:
                # This cannot happen for a quadratic residue, but we
                # keep the guard to avoid an infinite loop if the
                # caller violates the prime precondition.
                return None

        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i

    return r
