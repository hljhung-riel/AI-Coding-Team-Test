"""Unit tests for the multiply() function in src/agent_smoke_test.py.

These tests use Python's built-in unittest framework only, so the file can be
run directly from the repository root with:

    python -m unittest tests.test_agent_smoke -v

Import strategy
---------------
The project has no packages, installable distribution, or configured ``sys.path``
hints, and the module lives one directory below the repository root
(``src/agent_smoke_test.py``). To make the imports robust regardless of how the
test is invoked (``python -m unittest``, ``python tests/test_agent_smoke.py``,
or from inside the ``tests`` directory), we:

1. Locate the repository root relative to the test file itself.
2. Insert it into ``sys.path`` before importing the module by name.
3. Fall back to importing ``agent_smoke_test`` (works when ``src/`` is already
   importable, e.g. when tests are run with the repo root on the path via an
   editor or CI configuration).

This keeps the test file self-contained without modifying any existing source
files or adding packaging metadata.
"""

import os
import sys
import unittest

# ---------------------------------------------------------------------------
# Make the repository root importable so that ``src.agent_smoke_test`` resolves.
# ---------------------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)  # parent of tests/

if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

try:
    from src.agent_smoke_test import multiply
except ImportError:  # pragma: no cover - fallback for unusual execution contexts
    from agent_smoke_test import multiply


class TestMultiplyPositiveNumbers(unittest.TestCase):
    """Tests for multiplying two positive integers."""

    def test_multiply_two_positive_integers(self):
        """Multiplying two positive integers returns their product."""
        self.assertEqual(multiply(3, 4), 12)

    def test_multiply_positive_integers_result_larger_than_factors(self):
        """Product of integers greater than 1 exceeds both factors."""
        self.assertGreater(multiply(7, 6), 7)
        self.assertGreater(multiply(7, 6), 6)
        self.assertEqual(multiply(7, 6), 42)

    def test_multiply_by_one_is_identity(self):
        """Multiplying by 1 returns the other operand unchanged."""
        self.assertEqual(multiply(17, 1), 17)
        self.assertEqual(multiply(1, 99), 99)


class TestMultiplyNegativeNumbers(unittest.TestCase):
    """Tests for multiplication involving negative numbers."""

    def test_multiply_negative_and_positive(self):
        """A negative times a positive yields a negative result."""
        self.assertEqual(multiply(-5, 3), -15)

    def test_multiply_two_negative_numbers(self):
        """Two negative numbers multiplied give a positive result."""
        self.assertEqual(multiply(-4, -6), 24)

    def test_multiply_two_negative_floats(self):
        """Two negative floats multiplied give a positive float result."""
        self.assertAlmostEqual(multiply(-1.5, -2.0), 3.0)

    def test_multiply_by_negative_one_negates(self):
        """Multiplying by -1 negates the operand."""
        self.assertEqual(multiply(8, -1), -8)
        self.assertEqual(multiply(-8, -1), 8)


class TestMultiplyByZero(unittest.TestCase):
    """Tests for multiplication by zero."""

    def test_multiply_by_zero_returns_zero(self):
        """Any number multiplied by zero is zero."""
        self.assertEqual(multiply(123, 0), 0)

    def test_multiply_zero_by_nonzero_returns_zero(self):
        """Zero multiplied by any number is zero."""
        self.assertEqual(multiply(0, -987), 0)

    def test_multiply_float_by_zero_returns_positive_zero(self):
        """A float multiplied by zero is zero (float result)."""
        result = multiply(2.5, 0)
        self.assertEqual(result, 0)
        self.assertIsInstance(result, float)


class TestMultiplyFloats(unittest.TestCase):
    """Tests for multiplying floating-point numbers with precision handling."""

    def test_multiply_two_floats(self):
        """Multiplying two floats returns their product (within float precision)."""
        self.assertAlmostEqual(multiply(2.5, 4.0), 10.0)

    def test_multiply_floats_with_fractional_result(self):
        """Fractional floats produce an approximate product (7 decimal places)."""
        self.assertAlmostEqual(multiply(0.1, 0.2), 0.02)

    def test_multiply_float_and_integer(self):
        """A float times an integer returns the expected product."""
        self.assertAlmostEqual(multiply(1.5, 4), 6.0)

    def test_multiply_small_floats(self):
        """Very small floats multiply correctly (no underflow at these magnitudes)."""
        self.assertAlmostEqual(multiply(1e-10, 1e-10), 1e-20)


if __name__ == "__main__":
    unittest.main()
