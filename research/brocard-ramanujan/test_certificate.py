import copy
from math import factorial
import unittest
from check_certificate import check, verify_primes

NODES = {"2": {"factors": [], "witness": None},
         "3": {"factors": [[2, 1]], "witness": 2},
         "13": {"factors": [[2, 2], [3, 1]], "witness": 2}}

class CertificateTests(unittest.TestCase):
    def certificate(self, lo=6, hi=6):
        return dict(lower=lo, upper=hi, primes=[13],
                    prime_certificates=copy.deepcopy(NODES), first_reject=[0]*(hi-lo+1))

    def test_known_nonsquare_excluded(self):
        self.assertEqual(check(self.certificate())["excluded_by_checked_obstruction"], 1)

    def test_known_solution_cannot_be_excluded(self):
        with self.assertRaises(ValueError):
            check(self.certificate(4, 4))

    def test_survivor_is_unresolved_not_a_solution(self):
        c = self.certificate()
        c["first_reject"] = [-1]
        result = check(c)
        self.assertEqual(result["unresolved_candidates"], [6])
        self.assertEqual(result["excluded_by_checked_obstruction"], 0)
        self.assertFalse(result["lean_end_to_end_verified"])

    def test_incomplete_prime_factorization_rejected(self):
        c = self.certificate()
        c["prime_certificates"]["13"]["factors"] = [[2, 2]]
        with self.assertRaises(ValueError):
            check(c)

    def test_forged_prime_or_witness_rejected(self):
        with self.assertRaises(ValueError):
            verify_primes({"2": NODES["2"], "3": NODES["3"],
                           "9": {"factors": [[2, 3]], "witness": 2}}, [9])
        c = self.certificate()
        c["prime_certificates"]["13"]["witness"] = 1
        with self.assertRaises(ValueError):
            check(c)

    def test_coverage_and_prime_window_constraints(self):
        c = self.certificate()
        c["first_reject"] = []
        with self.assertRaises(ValueError):
            check(c)
        c = self.certificate(13, 13)
        with self.assertRaises(ValueError):
            check(c)

    def test_all_single_prime_rejections_match_exact_small_factorials(self):
        # The checker must never reject an actual square; for these small
        # inputs compare its acceptance against directly enumerated residues.
        squares = {r*r % 13 for r in range(13)}
        for n in range(13):
            c = self.certificate(n, n)
            is_nonresidue = (factorial(n)+1) % 13 not in squares
            if is_nonresidue:
                self.assertEqual(check(c)["excluded_by_checked_obstruction"], 1)
            else:
                with self.assertRaises(ValueError):
                    check(c)

if __name__ == "__main__":
    unittest.main()
