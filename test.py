import unittest

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


if __name__ == "__main__":
    unittest.main()
