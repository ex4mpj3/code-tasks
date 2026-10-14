import unittest
from itertools import product

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
NOT_INT_VALUES = ("a", 2.0, None, True, False)


class ErrorMessageTestCase(unittest.TestCase):
    def assert_error(self, error_type, message, function, *arguments):
        with self.assertRaises(error_type) as error:
            function(*arguments)
        self.assertEqual(str(error.exception), message)


class TestZeroOne(ErrorMessageTestCase):
    """Набор тестов генерации строк"""

    def test_length_one(self):
        """Длина 1"""
        self.assertTrue(check_strings(generate_strings(1), 1))

    def test_length_two(self):
        """Длина 2"""
        self.assertTrue(check_strings(generate_strings(2), 2))

    def test_longer_lengths(self):
        """Длины от 3 до 20"""
        for length in range(3, 21):
            with self.subTest(length=length):
                strings = generate_strings(length)
                self.assertIsInstance(strings, list)
                self.assertTrue(check_strings(strings, length))

    def test_length_not_int(self):
        """Длина не целое"""
        for length in NOT_INT_VALUES:
            with self.subTest(length=length):
                self.assert_error(TypeError, LENGTH_NOT_INT, generate_strings, length)

    def test_length_not_positive(self):
        """Длина меньше единицы"""
        for length in (0, -1):
            with self.subTest(length=length):
                self.assert_error(ValueError, LENGTH_NOT_POS, generate_strings, length)


class TestBinomialCoefficient(ErrorMessageTestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_known_values_both(self):
        """Края и середина треугольника Паскаля у обеих функций"""
        cases = (
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (2, 1, 2),
            (6, 3, 20),
            (10, 0, 1),
            (10, 1, 10),
            (10, 9, 10),
            (10, 10, 1),
            (20, 10, 184756),
        )
        for function, (n, k, expected) in product(BINOMIAL_FUNCTIONS, cases):
            with self.subTest(function=function.__name__, n=n, k=k):
                result = function(n, k)
                self.assertIs(type(result), int)
                self.assertEqual(result, expected)

    def test_large_iter(self):
        """Большие n у итеративной функции"""
        cases = (
            (30, 20, 30045015),
            (100, 50, 100891344545564193334812497256),
            (100000, 2, 4999950000),
        )
        for n, k, expected in cases:
            with self.subTest(n=n, k=k):
                self.assertEqual(binomial_coefficient_iter(n, k), expected)

    def test_n_less_than_k(self):
        """n меньше k"""
        for function, (n, k) in product(BINOMIAL_FUNCTIONS, ((1, 2), (0, 1))):
            with self.subTest(function=function.__name__, n=n, k=k):
                self.assert_error(ValueError, N_LESS_THAN_K_ERROR_MSG, function, n, k)

    def test_n_is_not_int(self):
        """n не целое"""
        message = NOT_INT_VALUE_TEMPL.format("n")
        for function, n in product(BINOMIAL_FUNCTIONS, NOT_INT_VALUES):
            with self.subTest(function=function.__name__, n=n):
                self.assert_error(TypeError, message, function, n, 2)

    def test_k_is_not_int(self):
        """k не целое"""
        message = NOT_INT_VALUE_TEMPL.format("k")
        for function, k in product(BINOMIAL_FUNCTIONS, NOT_INT_VALUES):
            with self.subTest(function=function.__name__, k=k):
                self.assert_error(TypeError, message, function, 5, k)

    def test_n_is_negative(self):
        """n отрицательное"""
        message = NEGATIVE_VALUE_TEMPL.format("n")
        for function in BINOMIAL_FUNCTIONS:
            with self.subTest(function=function.__name__):
                self.assert_error(ValueError, message, function, -1, 0)

    def test_k_is_negative(self):
        """k отрицательное"""
        message = NEGATIVE_VALUE_TEMPL.format("k")
        for function in BINOMIAL_FUNCTIONS:
            with self.subTest(function=function.__name__):
                self.assert_error(ValueError, message, function, 5, -1)

    def test_n_checked_before_k(self):
        """Ошибки в n и в k одновременно, сообщение про n"""
        cases = (
            ("a", None, TypeError, NOT_INT_VALUE_TEMPL.format("n")),
            (-1, "a", ValueError, NEGATIVE_VALUE_TEMPL.format("n")),
            (-1, -1, ValueError, NEGATIVE_VALUE_TEMPL.format("n")),
        )
        for function, (n, k, error_type, message) in product(BINOMIAL_FUNCTIONS, cases):
            with self.subTest(function=function.__name__, n=n, k=k):
                self.assert_error(error_type, message, function, n, k)


if __name__ == "__main__":
    unittest.main()
