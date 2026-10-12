import math
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

    def test_length_one_five_seven(self):
        """Длина 1,5,7"""
        for length in (1, 5, 7):
            with self.subTest(length=length):
                self.assertTrue(check_strings(generate_strings(length), length))

    def test_length_zero(self):
        """Длина 0"""
        with self.assertRaises(ValueError) as error:
            generate_strings(0)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)

    def test_length_negative(self):
        """Проверка на отрицательную длину"""
        with self.assertRaises(ValueError) as error:
            generate_strings(-3)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)

    def test_length_other_types(self):
        """Проверка на стринги, пустоту и BOOL"""
        for length in ("5", None, True):
            with self.subTest(length=length):
                with self.assertRaises(TypeError) as error:
                    generate_strings(length)
                self.assertEqual(str(error.exception), LENGTH_NOT_INT)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_side_value(self):
        """крайние значения С(0,0), С(n,0) C(n,n)=1"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(0, 0), 1)
                for n in range(1, 10):
                    with self.subTest(n=n):
                        self.assertEqual(func(n, 0), 1)
                        self.assertEqual(func(n, n), 1)

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

    def test_errors_both(self):
        """Каждая ошибка"""
        cases = [
            (2.0, 1, TypeError, NOT_INT_VALUE_TEMPL.format("n")),
            (True, 0, TypeError, NOT_INT_VALUE_TEMPL.format("n")),
            (5, "a", TypeError, NOT_INT_VALUE_TEMPL.format("k")),
            (5, 1.0, TypeError, NOT_INT_VALUE_TEMPL.format("k")),
            (5, False, TypeError, NOT_INT_VALUE_TEMPL.format("k")),
            (-1, 0, ValueError, NEGATIVE_VALUE_TEMPL.format("n")),
            (-1, 5, ValueError, NEGATIVE_VALUE_TEMPL.format("n")),
            (5, -1, ValueError, NEGATIVE_VALUE_TEMPL.format("k")),
            (0, 1, ValueError, N_LESS_THAN_K_ERROR_MSG),
        ]
        for func in BINOMIAL_FUNCTIONS:
            for n, k, error_type, message in cases:
                with self.subTest(func=func.__name__, n=n, k=k):
                    with self.assertRaises(error_type) as error:
                        func(n, k)
                    self.assertEqual(str(error.exception), message)

    def test_against_math_comb(self):
        """Все C(n, k) при n до 20"""
        for func in BINOMIAL_FUNCTIONS:
            for n in range(21):
                for k in range(n + 1):
                    with self.subTest(func=func.__name__, n=n, k=k):
                        self.assertEqual(func(n, k), math.comb(n, k))


if __name__ == "__main__":
    unittest.main()
