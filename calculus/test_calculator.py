#!/usr/bin/env python3
"""
Test suite for Calculus CLI Calculator
Run: python test_calculator.py
"""

import sys
import math
import unittest

sys.path.insert(0, ".")
from calculator import (
    safe_eval, convert_units, add, subtract, multiply, divide,
    power, modulo, sqrt, cbrt, ln, log10, log2, factorial,
    fmt_result, MemoryBank, HistoryManager
)


class TestArithmetic(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=10)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(0, 5), -5)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 5), -10)
        self.assertEqual(multiply(0, 999), 0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertAlmostEqual(divide(1, 3), 0.3333333333, places=9)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(5, 0)

    def test_power(self):
        self.assertEqual(power(2, 10), 1024)
        self.assertEqual(power(3, 0), 1)
        self.assertAlmostEqual(power(2, 0.5), math.sqrt(2), places=10)

    def test_modulo(self):
        self.assertEqual(modulo(10, 3), 1)
        self.assertEqual(modulo(9, 3), 0)

    def test_modulo_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            modulo(5, 0)


class TestAdvancedMath(unittest.TestCase):
    def test_sqrt(self):
        self.assertEqual(sqrt(144), 12)
        self.assertAlmostEqual(sqrt(2), 1.41421356, places=7)

    def test_sqrt_negative(self):
        with self.assertRaises(ValueError):
            sqrt(-1)

    def test_cbrt(self):
        self.assertAlmostEqual(cbrt(27), 3.0, places=10)
        self.assertAlmostEqual(cbrt(-8), -2.0, places=10)

    def test_ln(self):
        self.assertAlmostEqual(ln(math.e), 1.0, places=10)
        self.assertAlmostEqual(ln(1), 0.0, places=10)

    def test_ln_invalid(self):
        with self.assertRaises(ValueError):
            ln(0)
        with self.assertRaises(ValueError):
            ln(-1)

    def test_log10(self):
        self.assertAlmostEqual(log10(1000), 3.0, places=10)
        self.assertAlmostEqual(log10(1), 0.0, places=10)

    def test_log2(self):
        self.assertAlmostEqual(log2(8), 3.0, places=10)
        self.assertAlmostEqual(log2(1), 0.0, places=10)

    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_factorial_non_integer(self):
        with self.assertRaises(ValueError):
            factorial(2.5)


class TestSafeEval(unittest.TestCase):
    def test_basic_expression(self):
        self.assertEqual(safe_eval("2 + 3"), 5)
        self.assertEqual(safe_eval("10 - 4"), 6)
        self.assertEqual(safe_eval("3 * 4"), 12)
        self.assertEqual(safe_eval("10 / 2"), 5)

    def test_operator_precedence(self):
        self.assertEqual(safe_eval("2 + 3 * 4"), 14)
        self.assertEqual(safe_eval("(2 + 3) * 4"), 20)

    def test_caret_power(self):
        self.assertEqual(safe_eval("2^10"), 1024)

    def test_constants(self):
        self.assertAlmostEqual(safe_eval("pi"), math.pi, places=10)
        self.assertAlmostEqual(safe_eval("e"), math.e, places=10)
        self.assertAlmostEqual(safe_eval("tau"), math.tau, places=10)

    def test_functions(self):
        self.assertAlmostEqual(safe_eval("sqrt(16)"), 4.0, places=10)
        self.assertAlmostEqual(safe_eval("abs(-5)"), 5.0, places=10)
        self.assertAlmostEqual(safe_eval("floor(3.7)"), 3.0, places=10)
        self.assertAlmostEqual(safe_eval("ceil(3.2)"), 4.0, places=10)

    def test_ans_substitution(self):
        self.assertEqual(safe_eval("ans + 5", ans=10), 15)
        self.assertEqual(safe_eval("ans * 2", ans=7), 14)

    def test_implicit_multiply(self):
        self.assertAlmostEqual(safe_eval("2pi"), 2 * math.pi, places=10)

    def test_complex_expression(self):
        result = safe_eval("sin(30)**2 + cos(30)**2")
        self.assertAlmostEqual(result, 1.0, places=10)

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            safe_eval("import os")
        with self.assertRaises(ValueError):
            safe_eval("open('/etc/passwd')")

    def test_nested_expressions(self):
        self.assertAlmostEqual(safe_eval("sqrt(sqrt(256))"), 4.0, places=10)
        self.assertAlmostEqual(safe_eval("log(exp(5))"), 5.0, places=10)


class TestUnitConverter(unittest.TestCase):
    def test_length(self):
        self.assertAlmostEqual(convert_units(1, "km", "m"), 1000, places=5)
        self.assertAlmostEqual(convert_units(1, "m", "cm"), 100, places=5)
        self.assertAlmostEqual(convert_units(1, "mi", "km"), 1.60934, places=4)

    def test_mass(self):
        self.assertAlmostEqual(convert_units(1, "kg", "g"), 1000, places=5)
        self.assertAlmostEqual(convert_units(1, "kg", "lb"), 2.20462, places=4)

    def test_temperature(self):
        self.assertAlmostEqual(convert_units(0, "c", "f"), 32.0, places=5)
        self.assertAlmostEqual(convert_units(100, "c", "f"), 212.0, places=5)
        self.assertAlmostEqual(convert_units(32, "f", "c"), 0.0, places=5)
        self.assertAlmostEqual(convert_units(0, "c", "k"), 273.15, places=5)

    def test_time(self):
        self.assertEqual(convert_units(1, "hr", "min"), 60)
        self.assertEqual(convert_units(1, "min", "sec"), 60)
        self.assertEqual(convert_units(1, "day", "hr"), 24)

    def test_digital(self):
        self.assertEqual(convert_units(1, "gb", "mb"), 1024)
        self.assertEqual(convert_units(1, "tb", "gb"), 1024)

    def test_unknown_conversion(self):
        with self.assertRaises(ValueError):
            convert_units(1, "xyz", "abc")


class TestMemoryBank(unittest.TestCase):
    def test_store_and_recall(self):
        mem = MemoryBank()
        mem.store(42.0)
        self.assertEqual(mem.recall(), 42.0)

    def test_add(self):
        mem = MemoryBank()
        mem.store(10.0)
        mem.add(5.0)
        self.assertEqual(mem.recall(), 15.0)

    def test_subtract(self):
        mem = MemoryBank()
        mem.store(10.0)
        mem.sub(3.0)
        self.assertEqual(mem.recall(), 7.0)

    def test_clear(self):
        mem = MemoryBank()
        mem.store(99.0)
        mem.clear()
        self.assertEqual(mem.recall(), 0.0)

    def test_initial_value(self):
        mem = MemoryBank()
        self.assertEqual(mem.recall(), 0.0)


class TestFormatting(unittest.TestCase):
    def test_integer_like(self):
        self.assertEqual(fmt_result(42.0), "42")
        self.assertEqual(fmt_result(1000.0), "1,000")

    def test_float(self):
        result = fmt_result(3.14159)
        self.assertIn("3.14159", result)

    def test_negative(self):
        self.assertEqual(fmt_result(-7.0), "-7")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  CALCULUS — Test Suite")
    print("="*60 + "\n")

    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    test_classes = [
        TestArithmetic, TestAdvancedMath, TestSafeEval,
        TestUnitConverter, TestMemoryBank, TestFormatting,
    ]
    for cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*60)
    if result.wasSuccessful():
        print(f"  ✓ All {result.testsRun} tests passed!")
    else:
        print(f"  ✖ {len(result.failures)} failed, {len(result.errors)} errors")
    print("="*60 + "\n")

    sys.exit(0 if result.wasSuccessful() else 1)
