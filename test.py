import random
import unittest
from itertools import product

from main import ErrorMessages, ProfitValueError, get_invest_distribution


def _realized_profit(matrix, distribution):
    profit = 0
    for project, lots in enumerate(distribution):
        if lots != 0:
            profit += matrix[lots - 1][project]
    return profit


def _assert_optimal_result(test_case, matrix, result, expected_profit):
    levels = len(matrix)
    projects = len(matrix[0])
    test_case.assertEqual(result.profit, expected_profit)
    test_case.assertEqual(len(result.distribution), projects)
    test_case.assertEqual(sum(result.distribution), levels)
    for lots in result.distribution:
        test_case.assertGreaterEqual(lots, 0)
        test_case.assertLessEqual(lots, levels)
    test_case.assertEqual(
        _realized_profit(matrix, result.distribution), expected_profit
    )


class TestInvestDistribution(unittest.TestCase):
    """Набор тестов распределения инвестиций"""

    def test_none(self):
        """Аргумент None"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution(None)
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_bool_value(self):
        """В клетке bool"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution([[1, True]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_empty(self):
        """Пустой список"""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_negative_profit(self):
        """Отрицательная прибыль"""
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distribution([[1, -1]])
        self.assertEqual(str(error.exception), ErrorMessages.NEG_PROFIT)
        self.assertEqual(error.exception.project_idx, 1)
        self.assertEqual(error.exception.row_idx, 0)

    def test_decreasing_profit(self):
        """Прибыль убывает по столбцу"""
        matrix = [[1, 1, 1], [2, 3, 2], [2, 2, 3]]
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distribution(matrix)
        self.assertEqual(str(error.exception), ErrorMessages.DECR_PROFIT)
        self.assertEqual(error.exception.project_idx, 1)
        self.assertEqual(error.exception.row_idx, 2)

    def test_single(self):
        """Один проект и один уровень"""
        matrix = [[1]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 1)

    def test_float_profit(self):
        """Прибыль задана числами float"""
        matrix = [[1.5, 2.0], [3.0, 4.5]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 4.5)

    def test_lecture_table(self):
        """Таблица с лекции: прибыль 73"""
        matrix = [
            [15, 18, 16, 17],
            [20, 22, 23, 19],
            [26, 28, 27, 25],
            [34, 33, 29, 31],
            [40, 39, 41, 37],
        ]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 73)

    def test_not_list(self):
        """Аргумент не список"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution((1, 2))
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_row_not_list(self):
        """Строка таблицы не список"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution([[1, 2], (3, 4)])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_string_value(self):
        """В клетке строка"""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution([[1, "2"]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_empty_row(self):
        """Таблица из пустой строки"""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([[]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_not_rect(self):
        """Строки разной длины"""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([[1, 2], [3]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_negative_profit_position(self):
        """Отрицательная прибыль в нижней строке"""
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distribution([[0, 0], [0, 0], [-2, 5]])
        self.assertEqual(str(error.exception), ErrorMessages.NEG_PROFIT)
        self.assertEqual(error.exception.project_idx, 0)
        self.assertEqual(error.exception.row_idx, 2)

    def test_equal_profit_allowed(self):
        """Неубывание: равные значения в столбце допустимы"""
        matrix = [[5, 1], [5, 1], [5, 1]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 6)

    def test_all_zero(self):
        """Нулевая прибыль"""
        matrix = [[0, 0], [0, 0]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 0)

    def test_one_project(self):
        """Один проект: все лоты в него"""
        matrix = [[1], [4], [9]]
        result = get_invest_distribution(matrix)
        self.assertEqual(result.distribution, [3])
        _assert_optimal_result(self, matrix, result, 9)

    def test_one_level(self):
        """Один лот: в проект с наибольшей прибылью"""
        matrix = [[3, 7, 5]]
        result = get_invest_distribution(matrix)
        self.assertEqual(result.distribution, [0, 1, 0])
        _assert_optimal_result(self, matrix, result, 7)

    def test_brute_force(self):
        """Сравнение с полным перебором на случайных таблицах"""
        rng = random.Random(42)
        for _ in range(200):
            levels = rng.randint(1, 5)
            projects = rng.randint(1, 4)
            columns = [
                sorted(rng.randint(0, 30) for _ in range(levels))
                for _ in range(projects)
            ]
            matrix = [list(row) for row in zip(*columns)]
            best = max(
                _realized_profit(matrix, plan)
                for plan in product(range(levels + 1), repeat=projects)
                if sum(plan) == levels
            )
            result = get_invest_distribution(matrix)
            _assert_optimal_result(self, matrix, result, best)


if __name__ == "__main__":
    unittest.main()
