import unittest
from src.tools import calculator

class CalculatorTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(calculator("12 * (3 + 2)"), 60)
    def test_division(self):
        self.assertEqual(calculator("10 / 2"), 5)
    def test_rejects_code(self):
        self.assertIn("Could not calculate", calculator("__import__('os').system('echo no')"))

if __name__ == "__main__":
    unittest.main()
