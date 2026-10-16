"""Check bounded Wilson-window exclusion certificates with integer arithmetic.
This is a computational checker, not an end-to-end Lean proof or fidelity approval.
"""
from math import gcd, prod

def verify_primes(nodes, requested):
    verified = set()
    visiting = set()
    def visit(p):
        if p in verified:
            return
        if not 2 <= p < 2**64 or p in visiting:
            raise ValueError("invalid or cyclic prime")
        node = nodes[str(p)]
        if p == 2:
            if node != {"factors": [], "witness": None}:
                raise ValueError("wrong base certificate")
            verified.add(p)
            return
        visiting.add(p)
        factors = node["factors"]
        if not factors or len({q for q, _ in factors}) != len(factors):
            raise ValueError("missing or duplicate factors")
        for q, exponent in factors:
            if not isinstance(exponent, int) or not 1 <= exponent <= 64 or not 2 <= q < p:
                raise ValueError("invalid factor")
            visit(q)
        if prod(q**e for q, e in factors) != p - 1:
            raise ValueError("factorization incomplete")
        a = node["witness"]
        if not isinstance(a, int) or not 1 < a < p or pow(a, p - 1, p) != 1:
            raise ValueError("bad Lucas witness")
        if any(gcd(pow(a, (p - 1)//q, p) - 1, p) != 1 for q, _ in factors):
            raise ValueError("Lucas order obstruction failed")
        visiting.remove(p)
        verified.add(p)
    for p in requested:
        visit(p)
    return verified

def check(certificate):
    lo, hi = certificate["lower"], certificate["upper"]
    if not (0 <= lo <= hi < 2**64) or hi - lo + 1 > 10000:
        raise ValueError("out of bounded scope")
    primes = certificate["primes"]
    if not primes or len(primes) > 32 or len(set(primes)) != len(primes):
        raise ValueError("bad prime list")
    if any(not hi < p < 2**64 or p == 2 or p - lo > 100000 for p in primes):
        raise ValueError("prime does not bound window")
    verify_primes(certificate["prime_certificates"], primes)
    choices = certificate["first_reject"]
    if len(choices) != hi - lo + 1 or any(type(x) is not int or not -1 <= x < len(primes) for x in choices):
        raise ValueError("witness coverage mismatch")
    checked = set()
    # Reconstruct backwards from Wilson, using one inverse per step.
    # The search instead uses a single inverse of the whole tail then scans forward.
    for index, p in enumerate(primes):
        value = p - 1
        for n in range(p - 1, lo - 1, -1):
            if n <= hi and choices[n-lo] == index:
                if pow((value + 1) % p, (p - 1)//2, p) != p - 1:
                    raise ValueError("claimed nonresidue is not a nonresidue")
                checked.add(n)
            if n > lo:
                value = value * pow(n, -1, p) % p
    expected = {lo+i for i, value in enumerate(choices) if value >= 0}
    if checked != expected:
        raise ValueError("missing verified obstruction")
    return {"lower": lo, "upper": hi, "checked_values": hi-lo+1,
            "excluded_by_checked_obstruction": len(checked),
            "unresolved_candidates": [lo+i for i, value in enumerate(choices) if value == -1],
            "scope": "this_interval_only", "lean_end_to_end_verified": False,
            "independent_fidelity_review": "pending", "certification": "none"}
