import unittest

from main import (
    LENGTH_NOT_INT,
    LENGTH_NOT_POS,
    N_LESS_THAN_K_ERROR_MSG,
    NEGATIVE_VALUE_TEMPL,
    NOT_INT_VALUE_TEMPL,
    binomial_coefficient_iter,
    binomial_coefficient_rec,
    generate_strings,
)
from strings_checker import check_strings

BINOMIAL_FUNCTIONS = (binomial_coefficient_iter, binomial_coefficient_rec)


class TestZeroOne(unittest.TestCase):
    """Набор тестов генерации строк"""

    def test_length_two(self):
        """Длина 2"""
        self.assertTrue(check_strings(generate_strings(2), 2))

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            generate_strings(2.0)
        self.assertEqual(str(error.exception), LENGTH_NOT_INT)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_n_less_than_k(self):
        """n меньше k"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_iter(1, 2)
        self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)

    def test_n_is_not_int(self):
        """n не целое"""
        with self.assertRaises(TypeError) as error:
            binomial_coefficient_rec("a", 2)
        self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("n"))

class TestAdditionalZeroOne(unittest.TestCase):
    """Дополнительные проверки генерации строк."""

    def test_valid_lengths(self):
        for length in (1, 3, 4, 5, 10):
            with self.subTest(length=length):
                self.assertTrue(check_strings(generate_strings(length), length))

    def test_length_one_exact_strings(self):
        self.assertCountEqual(generate_strings(1), ["0", "1"])

    def test_length_three_exact_strings(self):
        self.assertCountEqual(generate_strings(3), ["010", "011", "101", "110", "111"])

    def test_invalid_nonpositive_lengths(self):
        for length in (0, -1, -10):
            with self.subTest(length=length):
                with self.assertRaises(ValueError) as error:
                    generate_strings(length)
                self.assertEqual(str(error.exception), LENGTH_NOT_POS)


    def test_invalid_length_types(self):
        for length in (2.5, "3", None, True, False, [3]):
            with self.subTest(length=length):
                with self.assertRaises(TypeError) as error:
                    generate_strings(length)
                self.assertEqual(str(error.exception), LENGTH_NOT_INT)


class TestAdditionalBinomialCoefficient(unittest.TestCase):
    """Проверки вычислений и обработки ошибок для обеих реализаций."""

    def test_known_values(self):
        cases = (
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (5, 0, 1),
            (5, 5, 1),
            (6, 1, 6),
            (6, 5, 6),
            (10, 3, 120),
            (10, 7, 120),
            (20, 10, 184756),
            (30, 20, 30045015),
        )
        for func in BINOMIAL_FUNCTIONS:
            for n, k, expected in cases:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), expected)

    def test_pascal_identity(self):
        for func in BINOMIAL_FUNCTIONS:
            for n in range(2, 13):
                for k in range(1, n):
                    with self.subTest(func=func.__name__, n=n, k=k):
                        self.assertEqual(func(n, k), func(n - 1, k - 1) + func(n - 1, k))

    def test_symmetry(self):
        for func in BINOMIAL_FUNCTIONS:
            for n in range(0, 16):
                for k in range(0, n + 1):
                    with self.subTest(func=func.__name__, n=n, k=k):
                        self.assertEqual(func(n, k), func(n, n - k))

    def test_invalid_types_for_both_parameters(self):
        for func in BINOMIAL_FUNCTIONS:
            for parameter in ("n", "k"):
                for bad_value in (1.0, "2", None, True, False, [2]):
                    args = {"n": 3, "k": 2}
                    args[parameter] = bad_value
                    with self.subTest(func=func.__name__, parameter=parameter, value=bad_value):
                        with self.assertRaises(TypeError) as error:
                            func(**args)
                        self.assertEqual(
                            str(error.exception), NOT_INT_VALUE_TEMPL.format(parameter)
                        )

    def test_negative_values_for_both_parameters(self):
        for func in BINOMIAL_FUNCTIONS:
            for parameter in ("n", "k"):
                for bad_value in (-1, -5):
                    args = {"n": 3, "k": 2}
                    args[parameter] = bad_value
                    with self.subTest(func=func.__name__, parameter=parameter, value=bad_value):
                        with self.assertRaises(ValueError) as error:
                            func(**args)
                        self.assertEqual(
                            str(error.exception), NEGATIVE_VALUE_TEMPL.format(parameter)
                        )

    def test_n_less_than_k_for_both_implementations(self):
        for func in BINOMIAL_FUNCTIONS:
            for n, k in ((0, 1), (1, 2), (3, 9)):
                with self.subTest(func=func.__name__, n=n, k=k):
                    with self.assertRaises(ValueError) as error:
                        func(n, k)
                    self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)




if __name__ == "__main__":
    unittest.main()
