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

    def test_length_bool(self):
        """Длина — bool"""
        with self.assertRaises(TypeError) as error:
            get_triangle_path_count(True)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)

    def test_length_string(self):
        """Длина — строка"""
        with self.assertRaises(TypeError) as error:
            get_triangle_path_count("2")
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)

    def test_length_none(self):
        """Длина — None"""
        with self.assertRaises(TypeError) as error:
            get_triangle_path_count(None)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_INT)

    def test_length_negative(self):
        """Длина отрицательная"""
        with self.assertRaises(ValueError) as error:
            get_triangle_path_count(-1)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_POS)

    def test_length_zero(self):
        """Длина ноль"""
        with self.assertRaises(ValueError) as error:
            get_triangle_path_count(0)
        self.assertEqual(str(error.exception), PATH_LENGTH_NOT_POS)

    def test_various_lengths(self):
        """Сравнение с замкнутой формулой для нескольких длин"""
        for length in range(1, 21):
            with self.subTest(length=length):
                self.assertEqual(
                    get_triangle_path_count(length),
                    _closed_path_count(length),
                )


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

    def test_k_is_not_int(self):
        """k не целое"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func(5, 2.5)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))

    def test_bool_params(self):
        """bool не считается целым"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__, param="n"):
                with self.assertRaises(TypeError) as error:
                    func(True, 0)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("n"))
            with self.subTest(func=func.__name__, param="k"):
                with self.assertRaises(TypeError) as error:
                    func(5, False)
                self.assertEqual(str(error.exception), NOT_INT_VALUE_TEMPL.format("k"))

    def test_negative_n(self):
        """n отрицательный"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(-1, 0)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("n"))

    def test_negative_k(self):
        """k отрицательный"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(5, -1)
                self.assertEqual(str(error.exception), NEGATIVE_VALUE_TEMPL.format("k"))

    def test_n_less_than_k_both(self):
        """n меньше k у обеих функций"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(ValueError) as error:
                    func(3, 5)
                self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)

    def test_both_invalid(self):
        """Оба параметра неверны"""
        cases = [
            ((-1, -2), ValueError, NEGATIVE_VALUE_TEMPL.format("n")),
            (("a", "b"), TypeError, NOT_INT_VALUE_TEMPL.format("n")),
            ((1.5, 0.5), TypeError, NOT_INT_VALUE_TEMPL.format("n")),
        ]
        for func in BINOMIAL_FUNCTIONS:
            for args, exc_type, msg in cases:
                with self.subTest(func=func.__name__, args=args):
                    with self.assertRaises(exc_type) as error:
                        func(*args)
                    self.assertEqual(str(error.exception), msg)

    def test_n_is_none(self):
        """n равно None"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                with self.assertRaises(TypeError) as error:
                    func(None, 1)
                self.assertEqual(
                    str(error.exception),
                    NOT_INT_VALUE_TEMPL.format("n"),
                )

    def test_edge_cases(self):
        """Краевые случаи: C(0,0), C(n,0), C(n,n)"""
        cases = [(0, 0), (10, 0), (10, 10), (1, 0), (1, 1)]
        for func in BINOMIAL_FUNCTIONS:
            for n, k in cases:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), 1)

    def test_regular_values(self):
        """Обычные значения"""
        cases = [(6, 3, 20), (15, 7, 6435)]
        for func in BINOMIAL_FUNCTIONS:
            for n, k, expected in cases:
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), expected)

    def test_larger_values(self):
        """Большие значения"""
        for func in BINOMIAL_FUNCTIONS:
            with self.subTest(func=func.__name__):
                self.assertEqual(func(30, 20), 30045015)

    def test_vs_math_comb(self):
        """Сверка с math.comb на диапазоне 0 ≤ k ≤ n ≤ 20"""
        for func in BINOMIAL_FUNCTIONS:
            for n in range(21):
                for k in range(n + 1):
                    with self.subTest(func=func.__name__, n=n, k=k):
                        self.assertEqual(func(n, k), math.comb(n, k))


if __name__ == "__main__":
    unittest.main()
