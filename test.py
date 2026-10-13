import math
import unittest

from main import (
    N_LESS_THAN_K_ERROR_MSG,
    NEGATIVE_VALUE_TEMPL,
    NOT_INT_VALUE_TEMPL,
    PATH_LENGTH_NOT_INT,
    PATH_LENGTH_NOT_POS,
    binomial_coefficient_iter,
    binomial_coefficient_rec,
    get_triangle_path_count,
)

BINOMIAL_FUNCTIONS = (binomial_coefficient_iter, binomial_coefficient_rec)


def _closed_path_count(length: int) -> int:
    return (2**length + 2 * ((-1) ** length)) // 3


class TestTrianglePath(unittest.TestCase):
    """Набор тестов подсчёта маршрутов"""

    def test_length_two(self):
        """Длина 2"""
        self.assertEqual(get_triangle_path_count(2), 2)

    def test_length_not_int(self):
        """Длина не целое"""
        with self.assertRaises(TypeError) as error:
            get_triangle_path_count(2.0)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)


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


class TestBinomialCoefficientExtended(unittest.TestCase):
    """Дополнение команды: свойства, сверка реализаций, валидация"""

    def test_by_math_comb(self):
        """Сверка обеих реализаций с math.comb"""
        for n in range(0, 26):
            for k in range(0, n + 1):
                with self.subTest(func="iter", n=n, k=k):
                    self.assertEqual(binomial_coefficient_iter(n, k), math.comb(n, k))
                with self.subTest(func="rec", n=n, k=k):
                    self.assertEqual(binomial_coefficient_rec(n, k), math.comb(n, k))

    def test_boundary_columns(self):
        """C(n, 0) = C(n, n) = 1 и C(n, 1) = n"""
        for func in BINOMIAL_FUNCTIONS:
            self.assertEqual(func(0, 0), 1)
            for n in range(1, 21):
                with self.subTest(func=func.__name__, n=n):
                    self.assertEqual(func(n, 0), 1)
                    self.assertEqual(func(n, n), 1)
                    self.assertEqual(func(n, 1), n)

    def test_symmetry(self):
        """C(n, k) = C(n, n - k)"""
        for n in range(0, 21):
            for k in range(0, n + 1):
                with self.subTest(n=n, k=k):
                    self.assertEqual(
                        binomial_coefficient_iter(n, k),
                        binomial_coefficient_iter(n, n - k),
                    )

    def test_large_values(self):
        """Значения из main и больше"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(30, 20), 30045015)
                self.assertEqual(func(100, 50), 100891344545564193334812497256)

    def test_negative(self):
        """Отрицательные параметры"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__, param="n"):
                with self.assertRaises(ValueError) as error:
                    func(-1, 0)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("n"))
            with self.subTest(func=func.__name__, param="k"):
                with self.assertRaises(ValueError) as error:
                    func(0, -1)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))

    def test_k_is_not_int(self):
        """k не целое"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func(2, True)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))

    def test_n_less_than_k_both(self):
        """n меньше k у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(1, 2)
                self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)


class TestTrianglePathExtended(unittest.TestCase):
    """Дополнение команды: таблица из условия и краевые случаи"""

    def test_table_values(self):
        """Значения из таблицы условия: a(1..4) = 0, 2, 2, 6"""
        for length, expected in ((1, 0), (2, 2), (3, 2), (4, 6)):
            with self.subTest(length=length):
                self.assertEqual(get_triangle_path_count(length), expected)

    def test_length_less_than_one(self):
        """Длина меньше единицы"""
        for value in (0, -1, -10):
            with self.subTest(value=value):
                with self.assertRaises(ValueError) as error:
                    get_triangle_path_count(value)
                self.assertEqual(str(error.exception), PATH_LENGTH_NOT_POS)


if __name__ == "__main__":
    unittest.main()
