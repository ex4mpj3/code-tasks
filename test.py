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

    def test_length_one(self):
        """Длина 1"""
        self.assertTrue(check_strings(generate_strings(1), 1))

    def test_length_five(self):
        """Длина 5"""
        self.assertTrue(check_strings(generate_strings(5), 5))

    def test_length_bool(self):
        """Длина логическое значение"""
        for length in (True, False):
            with self.subTest(length=length):
                with self.assertRaises(TypeError) as error:
                    generate_strings(length)
                self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_zero(self):
        """Длина равна нулю"""
        with self.assertRaises(ValueError) as error:
            generate_strings(0)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)

    def test_length_negative(self):
        """Длина отрицательная"""
        with self.assertRaises(ValueError) as error:
            generate_strings(-3)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)


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

    def test_binomial_values(self):
        """Разные значения биномиального коэффициента"""
        test_cases = (
            (0, 0, 1),
            (5, 0, 1),
            (5, 5, 1),
            (5, 1, 5),
            (6, 3, 20),
            (8, 2, 28),
            (10, 4, 210),
            (20, 8, 125970),
        )

        for function in BINOMIAL_FUNCTIONS:
            for n, k, expected in test_cases:
                with self.subTest(function=function.__name__, n=n, k=k):
                    self.assertEqual(function(n, k), expected)

    def test_n_less_than_k_rec(self):
        """n меньше k у рекурсивной функции"""
        with self.assertRaises(ValueError) as error:
            binomial_coefficient_rec(1, 2)
        self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)

    def test_k_is_not_int(self):
        """k не целое"""
        for function in BINOMIAL_FUNCTIONS:
            with self.subTest(function=function.__name__):
                with self.assertRaises(TypeError) as error:
                    function(5, 2.0)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))

    def test_bool_arguments(self):
        """n или k логическое значение"""
        for function in BINOMIAL_FUNCTIONS:
            for n, k, parameter in ((True, 1, "n"), (3, False, "k")):
                with self.subTest(function=function.__name__, parameter=parameter):
                    with self.assertRaises(TypeError) as error:
                        function(n, k)
                    self.assertEqual(
                        str(error.exception), NOT_INT_VALUE_TEMPL.format(parameter)
                    )

    def test_negative_n(self):
        """n отрицательное"""
        for function in BINOMIAL_FUNCTIONS:
            with self.subTest(function=function.__name__):
                with self.assertRaises(ValueError) as error:
                    function(-1, 0)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("n"))

    def test_negative_k(self):
        """k отрицательное"""
        for function in BINOMIAL_FUNCTIONS:
            with self.subTest(function=function.__name__):
                with self.assertRaises(ValueError) as error:
                    function(4, -1)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))


if __name__ == "__main__":
    unittest.main()
