"""Tests for the Tonelli-Shanks implementation."""

import unittest

from modular_square_root import modular_sqrt


class ModularSqrtTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(modular_sqrt(0, 7), 0)

    def test_small_prime_2(self):
        self.assertEqual(modular_sqrt(0, 2), 0)
        self.assertEqual(modular_sqrt(1, 2), 1)

    def test_simple_case_p_mod_4_equals_3(self):
        # p = 7 is 3 mod 4
        roots = set()
        for a in range(7):
            root = modular_sqrt(a, 7)
            if root is None:
                # Check that no square equals a mod 7
                self.assertNotIn(a, {x * x % 7 for x in range(7)})
            else:
                self.assertIn(a, {x * x % 7 for x in range(7)})
                self.assertEqual(root * root % 7, a)

    def test_tonelli_shanks_case_p_mod_4_equals_1(self):
        # p = 13 is 1 mod 4
        residues = {x * x % 13 for x in range(13)}
        for a in range(13):
            root = modular_sqrt(a, 13)
            if a in residues:
                self.assertIsNotNone(root)
                self.assertEqual(root * root % 13, a)
            else:
                self.assertIsNone(root)

    def test_larger_prime(self):
        p = 101  # 1 mod 4
        residues = {x * x % p for x in range(p)}
        for a in [0, 1, 2, 4, 10, 50, 100]:
            root = modular_sqrt(a, p)
            if a in residues:
                self.assertIsNotNone(root)
                self.assertEqual(root * root % p, a)
            else:
                self.assertIsNone(root)

    def test_negative_input_is_reduced_modulo_p(self):
        p = 17
        # -1 ≡ 16 mod 17, and 16 is a square (4^2)
        root = modular_sqrt(-1, p)
        self.assertIsNotNone(root)
        self.assertEqual(root * root % p, 16)

    def test_non_residue_returns_none(self):
        self.assertIsNone(modular_sqrt(2, 3))
        self.assertIsNone(modular_sqrt(3, 5))
        self.assertIsNone(modular_sqrt(5, 7))

    def test_invalid_modulus_raises(self):
        with self.assertRaises(ValueError):
            modular_sqrt(1, 1)
        with self.assertRaises(ValueError):
            modular_sqrt(1, 4)

    def test_returned_root_is_in_range(self):
        p = 97
        for a in [0, 1, 3, 10, 35, 96]:
            root = modular_sqrt(a, p)
            if root is not None:
                self.assertGreaterEqual(root, 0)
                self.assertLess(root, p)

    def test_root_consistent_for_square_numbers(self):
        p = 29
        for x in range(1, p):
            a = x * x % p
            root = modular_sqrt(a, p)
            self.assertIsNotNone(root)
            self.assertEqual(root * root % p, a)


if __name__ == "__main__":
    unittest.main()
