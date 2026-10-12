import unittest
from itertools import combinations, product

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

    def test_explicit_small_sets(self):
        """Проверяет точные ответы, тип списка и отсутствие повторов при n=1..4."""
        cases = (
            (1, ["0", "1"]),
            (2, ["01", "10", "11"]),
            (3, ["010", "011", "101", "110", "111"]),
            (4, ["0101", "0110", "0111", "1010", "1011", "1101", "1110", "1111"]),
        )
        for length, expected in cases:
            with self.subTest(length=length):
                result = generate_strings(length)
                self.assertIsInstance(result, list)
                self.assertCountEqual(result, expected)

    def test_complete_sets_by_exhaustive_search(self):
        """Сверяет n=5..8 с полным перебором, обнаруживая пропуски и дубликаты."""
        for length in range(5, 9):
            with self.subTest(length=length):
                candidates = ("".join(bits) for bits in product("01", repeat=length))
                expected = [
                    candidate for candidate in candidates if "00" not in candidate
                ]
                result = generate_strings(length)
                self.assertIsInstance(result, list)
                self.assertCountEqual(result, expected)

    def test_length_two(self):
        """Проверяет результат для длины 2 штатным валидатором задания."""
        self.assertTrue(check_strings(generate_strings(2), 2))

    def test_length_not_int(self):
        """Отклоняет нецелую длину, включая оба булевых значения."""
        for length in (2.0, "2", None, True, False, [], {}):
            with self.subTest(length=length):
                with self.assertRaises(TypeError) as error:
                    generate_strings(length)
                self.assertEqual(str(error.exception), LENGTH_NOT_INT)

    def test_length_less_than_one(self):
        """Отклоняет нулевую и отрицательную длину с сообщением задания."""
        for length in (0, -1, -5):
            with self.subTest(length=length):
                with self.assertRaises(ValueError) as error:
                    generate_strings(length)
                self.assertEqual(str(error.exception), LENGTH_NOT_POS)


class TestBinomialCoefficient(unittest.TestCase):
    """Набор тестов биномиального коэффициента"""

    def test_small_both(self):
        """Проверяет явно заданные строки треугольника, включая C(0, 0)."""
        expected_rows = (
            (1,),
            (1, 1),
            (1, 2, 1),
            (1, 3, 3, 1),
            (1, 4, 6, 4, 1),
            (1, 5, 10, 10, 5, 1),
            (1, 6, 15, 20, 15, 6, 1),
        )
        for func in BINOMIAL_FUNCTIONS:
            for n, row in enumerate(expected_rows):
                for k, expected in enumerate(row):
                    with self.subTest(func=func.__name__, n=n, k=k):
                        result = func(n, k)
                        self.assertIs(type(result), int)
                        self.assertEqual(result, expected)

    def test_counting_combinations(self):
        """Сверяет n=7..10 с числом подмножеств без повторения правила Паскаля."""
        for n in range(7, 11):
            for k in range(n + 1):
                expected = len(list(combinations(range(n), k)))
                for func in BINOMIAL_FUNCTIONS:
                    with self.subTest(func=func.__name__, n=n, k=k):
                        result = func(n, k)
                        self.assertIs(type(result), int)
                        self.assertEqual(result, expected)

    def test_boundary_columns(self):
        """Проверяет крайние столбцы и соседние с ними значения при большем n."""
        for func in BINOMIAL_FUNCTIONS:
            for n, k, expected in (
                (100, 0, 1),
                (100, 100, 1),
                (30, 1, 30),
                (30, 29, 30),
            ):
                with self.subTest(func=func.__name__, n=n, k=k):
                    self.assertEqual(func(n, k), expected)

    def test_large_integer_iterative(self):
        """Проверяет итеративный результат больше 64-битного целого без округления."""
        result = binomial_coefficient_iter(100, 50)
        self.assertIs(type(result), int)
        self.assertEqual(result, 100891344545564193334812497256)

    def test_n_less_than_k(self):
        """Обе функции отклоняют k > n, в том числе при n=0."""
        for func in BINOMIAL_FUNCTIONS:
            for n, k in ((0, 1), (1, 2), (3, 5)):
                with self.subTest(func=func.__name__, n=n, k=k):
                    with self.assertRaises(ValueError) as error:
                        func(n, k)
                    self.assertEqual(str(error.exception), N_LESS_THAN_K_ERROR_MSG)

    def test_n_is_not_int(self):
        """Обе функции отклоняют нецелый n, включая bool."""
        for func in BINOMIAL_FUNCTIONS:
            for n in (2.0, "2", None, True, False, [], {}):
                with self.subTest(func=func.__name__, n=n):
                    with self.assertRaises(TypeError) as error:
                        func(n, 0)
                    self.assertEqual(
                        str(error.exception), NOT_INT_VALUE_TEMPL.format("n")
                    )

    def test_k_is_not_int(self):
        """Обе функции отклоняют нецелый k, включая bool."""
        for func in BINOMIAL_FUNCTIONS:
            for k in (2.0, "2", None, True, False, [], {}):
                with self.subTest(func=func.__name__, k=k):
                    with self.assertRaises(TypeError) as error:
                        func(2, k)
                    self.assertEqual(
                        str(error.exception), NOT_INT_VALUE_TEMPL.format("k")
                    )

    def test_negative_n(self):
        """Обе функции отклоняют отрицательный n с одинаковым сообщением."""
        for func in BINOMIAL_FUNCTIONS:
            for n in (-1, -5):
                with self.subTest(func=func.__name__, n=n):
                    with self.assertRaises(ValueError) as error:
                        func(n, 0)
                    self.assertEqual(
                        str(error.exception), NEGATIVE_VALUE_TEMPL.format("n")
                    )

    def test_negative_k(self):
        """Обе функции отклоняют отрицательный k с одинаковым сообщением."""
        for func in BINOMIAL_FUNCTIONS:
            for k in (-1, -5):
                with self.subTest(func=func.__name__, k=k):
                    with self.assertRaises(ValueError) as error:
                        func(2, k)
                    self.assertEqual(
                        str(error.exception), NEGATIVE_VALUE_TEMPL.format("k")
                    )


if __name__ == "__main__":
    unittest.main()
