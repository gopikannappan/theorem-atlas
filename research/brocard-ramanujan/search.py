"""One bounded Brocard-Ramanujan research attempt; no global completeness claim."""
import hashlib
import json
from math import factorial, gcd, isqrt
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_certificate import check

LOWER = 2**61 - 1 - 10000
UPPER = 2**61 - 2
PRIME_COUNT = 32
EXACT_UPPER = 2000

def tail_residue(n, p):
    if not 0 <= n < p:
        raise ValueError("Wilson tail requires n < p")
    tail = 1
    for k in range(n + 1, p):
        tail = tail * k % p
    return -pow(tail, -1, p) % p

def make_prime_certificates(primes):
    from sympy import factorint
    nodes = {}
    def certify(p):
        if str(p) in nodes:
            return
        if p == 2:
            nodes["2"] = {"factors": [], "witness": None}
            return
        factors = sorted((int(q), int(e)) for q, e in factorint(p - 1).items())
        for q, _ in factors:
            certify(q)
        for a in range(2, min(p, 10002)):
            if pow(a, p - 1, p) == 1 and all(gcd(pow(a, (p - 1)//q, p) - 1, p) == 1 for q, _ in factors):
                nodes[str(p)] = {"factors": factors, "witness": a}
                return
        raise RuntimeError("bounded witness generation failed")
    for p in primes:
        certify(p)
    return nodes

def main():
    from sympy import nextprime
    import sympy
    started = time.monotonic()
    out = Path("brocard-evidence")
    out.mkdir(exist_ok=True)
    checkpoint = {"state": "started", "lower": LOWER, "upper": UPPER,
                  "prime_count": PRIME_COUNT, "exact_upper": EXACT_UPPER,
                  "certification": "none"}
    (out / "checkpoint.json").write_text(json.dumps(checkpoint, indent=2) + "\n")
    # Exact full-integer baseline, including zero as a boundary check.
    fact = 1
    solutions = []
    for n in range(EXACT_UPPER + 1):
        if n:
            fact *= n
        root = isqrt(fact + 1)
        if root * root == fact + 1:
            solutions.append([n, root])
    if solutions != [[4, 5], [5, 11], [7, 71]]:
        raise RuntimeError("baseline differs from expected solutions; investigate")
    # Exhaustive cross-check of Wilson tails against exact factorials at small primes.
    cross_checks = 0
    p = 2
    while p < 100:
        for n in range(p):
            if tail_residue(n, p) != factorial(n) % p:
                raise RuntimeError("Wilson-tail cross-check failed")
            cross_checks += 1
        p = int(nextprime(p))
    primes = []
    p = int(nextprime(UPPER))
    for _ in range(PRIME_COUNT):
        primes.append(p)
        p = int(nextprime(p))
    nodes = make_prime_certificates(primes)
    checkpoint.update(state="prime_certificates_generated", primes=primes)
    (out / "checkpoint.json").write_text(json.dumps(checkpoint, indent=2) + "\n")
    residues = [tail_residue(LOWER, p) for p in primes]
    first_reject = []
    rejection_counts = [0] * len(primes)
    for n in range(LOWER, UPPER + 1):
        if n > LOWER:
            residues = [value * n % p for value, p in zip(residues, primes)]
        rejected = -1
        for index, (value, p) in enumerate(zip(residues, primes)):
            if pow((value + 1) % p, (p - 1)//2, p) == p - 1:
                rejected = index
                rejection_counts[index] += 1
                break
        first_reject.append(rejected)
    certificate = {"schema_version": 1, "lower": LOWER, "upper": UPPER,
                   "primes": primes, "prime_certificates": nodes, "first_reject": first_reject}
    raw = json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n"
    (out / "certificate.json").write_text(raw)
    # Do not expose an accepted range until the separate stdlib checker passes.
    verification = check(certificate)
    report = {"schema_version": 1, "state": "bounded_attempt_complete",
              "exact_baseline": {"lower": 0, "upper": EXACT_UPPER, "solutions": solutions},
              "tail_cross_checks": cross_checks, "targeted_window": verification,
              "primes": primes, "rejection_counts": rejection_counts,
              "certificate_sha256": hashlib.sha256(raw.encode()).hexdigest(),
              "sympy_version": sympy.__version__, "elapsed_seconds": time.monotonic()-started,
              "new_solution_found": False,
              "new_solution_search_status": "no_new_solution_identified; survivors_if_any_remain_unresolved",
              "global_problem_status": "open", "novelty": "not_established",
              "scope": "exact_small_baseline_and_named_large_interval_only",
              "certification": "none"}
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    (out / "checkpoint.json").write_text(json.dumps(dict(checkpoint, state="complete"), indent=2) + "\n")
    print("BROCARD_CERTIFICATE " + raw.strip())
    print("BROCARD_REPORT " + json.dumps(report))

if __name__ == "__main__":
    main()
