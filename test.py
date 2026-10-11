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

    def test_length_one(self):
        """Длина 1"""
        self.assertEqual(get_triangle_path_count(1), 0)

    def test_length_two(self):
        """Длина 2"""
        self.assertEqual(get_triangle_path_count(2), 2)

    def test_table_values(self):
        """Значения из таблицы в условии"""
        self.assertEqual(get_triangle_path_count(3), 2)
        self.assertEqual(get_triangle_path_count(4), 6)

    def test_by_formula(self):
        """Проверка по формуле для разных длин"""
        for length in range(1, 10):
            with self.subTest(length=length):
                self.assertEqual(
                    get_triangle_path_count(length),
                    _closed_path_count(length),
                )

    def test_length_not_int(self):
        """Длина не целое"""
        for val in (2.0, "3", None, True, False):
            with self.subTest(val=val):
                with self.assertRaises(TypeError) as error:
                    get_triangle_path_count(val)
                self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)

    def test_length_less_than_one(self):
        """Длина меньше единицы"""
        for val in (0, -1, -5):
            with self.subTest(val=val):
                with self.assertRaises(ValueError) as error:
                    get_triangle_path_count(val)
                self.assertEqual(str(error.exception), PATH_LENGTH_NOT_POS)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """C(5, 2) у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(5, 2), 10)

    def test_edge_cases(self):
        """Граничные значения k = 0 и k = n"""
        cases = ((0, 0, 1), (5, 0, 1), (5, 5, 1), (6, 1, 6))
        for func in BINOMIAL_FUNCTIONS:
            for n, k, res in cases:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), res)

    def test_large_values(self):
        """Проверка на больших числах"""
        cases = ((10, 3, 120), (20, 10, 184756), (30, 20, 30045015))
        for func in BINOMIAL_FUNCTIONS:
            for n, k, res in cases:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), res)

    def test_n_less_than_k(self):
        """n меньше k"""
        for func in BINOMIAL_FUNCTIONS:
            for n, k in ((1, 2), (0, 1), (5, 10)):
                with self.subTest(func=func.__name__, n=n, k=k):
                    with self.assertRaises(ValueError) as error:
                        func(n, k)
                    self.assertEqual(
                        str(error.exception),
                        N_LESS_THAN_K_ERROR_MSG,
                    )

    def test_n_is_not_int(self):
        """n не целое"""
        for func in BINOMIAL_FUNCTIONS:
            for val in ("a", 2.5, None, True, False):
                with self.subTest(func=func.__name__, val=val):
                    with self.assertRaises(TypeError) as error:
                        func(val, 2)
                    self.assertEqual(
                        str(error.exception),
                        NOT_INT_VALUE_TEMPL.format("n"),
                    )

    def test_k_is_not_int(self):
        """k не целое"""
        for func in BINOMIAL_FUNCTIONS:
            for val in ("b", 1.5, None, True, False):
                with self.subTest(func=func.__name__, val=val):
                    with self.assertRaises(TypeError) as error:
                        func(5, val)
                    self.assertEqual(
                        str(error.exception),
                        NOT_INT_VALUE_TEMPL.format("k"),
                    )

    def test_negative_n(self):
        """n отрицательный"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(-3, 1)
                self.assertEqual(
                    str(error.exception),
                    NEGATIVE_VALUE_TEMPL.format("n"),
                )

    def test_negative_k(self):
        """k отрицательный"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(5, -2)
                self.assertEqual(
                    str(error.exception),
                    NEGATIVE_VALUE_TEMPL.format("k"),
                )


if __name__ == "__main__":
    unittest.main()
