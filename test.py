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


class TestTrianglePathCount(unittest.TestCase):
    """Тесты для функции подсчета маршрутов в треугольнике."""

    def test_correct_values(self):
        # Длина 1: из A в A путей нет.
        self.assertEqual(get_triangle_path_count(1), 0)
        # Длина 2: ABA, ACA.
        self.assertEqual(get_triangle_path_count(2), 2)
        # Длина 3: ABCA, ACBA.
        self.assertEqual(get_triangle_path_count(3), 2)
        # Формула: (2**n + 2 * (-1)**n) // 3.
        self.assertEqual(get_triangle_path_count(4), 6)
        self.assertEqual(get_triangle_path_count(5), 10)

    def test_invalid_types(self):
        # Проверка на нецелое число.
        with self.assertRaisesRegex(TypeError, PATH_LENGTH_NOT_INT):
            get_triangle_path_count(2.5)
        with self.assertRaisesRegex(TypeError, PATH_LENGTH_NOT_INT):
            get_triangle_path_count("4")

    def test_invalid_values(self):
        # Проверка на длину меньше 1.
        with self.assertRaisesRegex(ValueError, PATH_LENGTH_NOT_POS):
            get_triangle_path_count(0)
        with self.assertRaisesRegex(ValueError, PATH_LENGTH_NOT_POS):
            get_triangle_path_count(-5)


class TestBinomialCoefficient(unittest.TestCase):
    """Тесты итеративного и рекурсивного биномиального коэффициента."""

    def test_correct_values(self):
        functions = [binomial_coefficient_iter, binomial_coefficient_rec]

        for func in functions:
            # Из 5 по 2 = 10.
            self.assertEqual(func(5, 2), 10)
            # Из 30 по 20 = 30045015.
            self.assertEqual(func(30, 20), 30045015)
            # Граничный случай: k = 0.
            self.assertEqual(func(5, 0), 1)
            # Граничный случай: n = k.
            self.assertEqual(func(5, 5), 1)

    def test_invalid_types(self):
        functions = [binomial_coefficient_iter, binomial_coefficient_rec]

        for func in functions:
            # Ошибка в параметре n.
            with self.assertRaisesRegex(
                TypeError, NOT_INT_VALUE_TEMPL.format("n")
            ):
                func(5.5, 2)
            # Ошибка в параметре k.
            with self.assertRaisesRegex(
                TypeError, NOT_INT_VALUE_TEMPL.format("k")
            ):
                func(5, "2")

    def test_invalid_values(self):
        functions = [binomial_coefficient_iter, binomial_coefficient_rec]

        for func in functions:
            # Отрицательный n.
            with self.assertRaisesRegex(
                ValueError, NEGATIVE_VALUE_TEMPL.format("n")
            ):
                func(-5, 2)
            # Отрицательный k.
            with self.assertRaisesRegex(
                ValueError, NEGATIVE_VALUE_TEMPL.format("k")
            ):
                func(5, -2)
            # Условие n < k.
            with self.assertRaisesRegex(ValueError, N_LESS_THAN_K_ERROR_MSG):
                func(2, 5)


if __name__ == "__main__":
    unittest.main()