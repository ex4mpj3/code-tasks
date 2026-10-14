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

    def test_return_type(self):
        """Возвращается список строк"""
        res = generate_strings(2)
        self.assertIsInstance(res, list)
        for item in res:
            self.assertIsInstance(item, str)

    def test_length_type(self):
        """Длина не тип целого числа"""
        for length in (None, "1", True, False):
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
        """Длина меньше нуля"""
        with self.assertRaises(ValueError) as error:
            generate_strings(-3)
        self.assertEqual(str(error.exception), LENGTH_NOT_POS)

    def test_length_one(self):
        """Длина 1"""
        self.assertCountEqual(generate_strings(1), ["0", "1"])

    def test_length_three(self):
        """Длина 3, пример из лекции"""
        self.assertCountEqual(generate_strings(3), ["010", "011", "110", "101", "111"])

    def test_lengths_checker(self):
        """Полный набор строк для длин от 1 до 15"""
        for length in range(1, 16):
            with self.subTest(length=length):
                self.assertTrue(check_strings(generate_strings(length), length))

    def test_no_double_zero(self):
        """Нет двух нулей подряд и нет повторов"""
        res = generate_strings(8)
        self.assertEqual(len(res), len(set(res)))
        for s in res:
            with self.subTest(s=s):
                self.assertNotIn("00", s)


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

    def test_invalid_types(self):
        """Типы параметров"""
        for func in BINOMIAL_FUNCTIONS:
            for value in (None, 1.0, True, False):
                with self.subTest(func=func.__name__, n=value):
                    with self.assertRaises(TypeError) as error:
                        func(value, 2)
                    self.assertEqual(
                        str(error.exception), NOT_INT_VALUE_TEMPL.format("n")
                    )
                with self.subTest(func=func.__name__, k=value):
                    with self.assertRaises(TypeError) as error:
                        func(1, value)
                    self.assertEqual(
                        str(error.exception), NOT_INT_VALUE_TEMPL.format("k")
                    )

    def test_negative(self):
        """Отрицательные значения"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(-3, 2)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("n"))
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(1, -3)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))

    def test_bases(self):
        """Базы C(n, 0) = C(n, n) = 1, в том числе C(0, 0)"""
        for func in BINOMIAL_FUNCTIONS:
            for n in range(0, 8):
                with self.subTest(func=func.__name__, n=n):
                    self.assertEqual(func(n, 0), 1)
                    self.assertEqual(func(n, n), 1)

    def test_known_values(self):
        """Известные значения"""
        cases = [(4, 2, 6), (6, 3, 20), (10, 3, 120), (20, 10, 184756)]
        for func in BINOMIAL_FUNCTIONS:
            for n, k, value in cases:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), value)

    def test_big_iter(self):
        """Большие значения итеративно"""
        self.assertEqual(binomial_coefficient_iter(30, 20), 30045015)
        self.assertEqual(binomial_coefficient_iter(60, 30), 118264581564861424)

    def test_iter_equals_rec(self):
        """Итеративная и рекурсивная функции совпадают"""
        for n in range(0, 15):
            for k in range(0, n + 1):
                with self.subTest(n=n, k=k):
                    self.assertEqual(
                        binomial_coefficient_iter(n, k), binomial_coefficient_rec(n, k)
                    )

    def test_row_sum(self):
        """Сумма строки треугольника Паскаля равна 2 в степени n"""
        for func in BINOMIAL_FUNCTIONS:
            for n in range(0, 12):
                with self.subTest(func=func.__name__, n=n):
                    total = 0
                    for k in range(n + 1):
                        total += func(n, k)
                    self.assertEqual(total, 2**n)

    def test_n_less_than_k_both(self):
        """n меньше k у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            for n, k in [(1, 2), (0, 1), (3, 10)]:
                with self.subTest(func=func.__name__, n=n, k=k):
                    with self.assertRaises(ValueError) as error:
                        func(n, k)
                    self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)

    def test_check_order(self):
        """Порядок проверок: сначала типы, потом знак, потом n < k"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func("a", -1)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("n"))
                with self.assertRaises(ValueError) as error:
                    func(-1, 5)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("n"))


if __name__ == "__main__":
    unittest.main()
