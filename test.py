import unittest

from main import ErrorMessages, ProfitValueError, get_invest_distributions


def _realized_profit(matrix, distribution):
    profit = 0
    for project, lots in enumerate(distribution):
        if lots != 0:
            profit += matrix[lots - 1][project]
    return profit


def _assert_all_optima(test_case, matrix, result, expected_profit, expected_count):
    levels = len(matrix)
    projects = len(matrix[0])
    test_case.assertEqual(result.profit, expected_profit)
    test_case.assertEqual(len(result.distributions), expected_count)
    seen = []
    for distribution in result.distributions:
        test_case.assertEqual(len(distribution), projects)
        test_case.assertEqual(sum(distribution), levels)
        for lots in distribution:
            test_case.assertGreaterEqual(lots, 0)
            test_case.assertLessEqual(lots, levels)
        test_case.assertEqual(_realized_profit(matrix, distribution), expected_profit)
        key = tuple(distribution)
        test_case.assertNotIn(key, seen)
        seen.append(key)


class TestInvestDistributions(unittest.TestCase):
    """Набор тестов всех оптимальных распределений"""

    def test_none(self):
        """Аргумент None"""
        with self.assertRaises(TypeError) as error:
            get_invest_distributions(None)
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_bool_value(self):
        """В клетке bool"""
        with self.assertRaises(TypeError) as error:
            get_invest_distributions([[1, True]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_not_list_of_lists(self):
        """Список чисел вместо списка списков"""
        with self.assertRaises(TypeError) as error:
            get_invest_distributions([1, 2, 3])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_string_value(self):
        """В клетке строка"""
        with self.assertRaises(TypeError) as error:
            get_invest_distributions([[1, "2"]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_empty(self):
        """Пустой список"""
        with self.assertRaises(ValueError) as error:
            get_invest_distributions([])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_empty_rows(self):
        """Список с пустыми строками"""
        with self.assertRaises(ValueError) as error:
            get_invest_distributions([[], []])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_jagged_matrix(self):
        """Непрямоугольная матрица (строки разной длины)"""
        with self.assertRaises(ValueError) as error:
            get_invest_distributions([[1, 2], [3, 4, 5]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_negative_profit(self):
        """Отрицательная прибыль"""
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distributions([[1, -1]])
        self.assertEqual(str(error.exception), ErrorMessages.NEG_PROFIT)
        self.assertEqual(error.exception.project_idx, 1)
        self.assertEqual(error.exception.row_idx, 0)

    def test_decreasing_profit(self):
        """Прибыль убывает по столбцу"""
        matrix = [[1, 1, 1], [2, 3, 2], [2, 2, 3]]
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distributions(matrix)
        self.assertEqual(str(error.exception), ErrorMessages.DECR_PROFIT)
        self.assertEqual(error.exception.project_idx, 1)
        self.assertEqual(error.exception.row_idx, 2)

    def test_single(self):
        """Один проект и один уровень"""
        matrix = [[1]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 1, 1)

    def test_one_project_multiple_lots(self):
        """Один проект и несколько лотов"""
        matrix = [[2], [5], [9]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 9, 1)

    def test_one_lot_multiple_projects(self):
        """Один лот и несколько проектов с двумя максимумами"""
        matrix = [[4, 7, 7, 2]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 7, 2)

    def test_zero_profits(self):
        """Нулевая прибыль: 2 лота по 2 проектам дают 3 плана"""
        matrix = [[0, 0], [0, 0]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 0, 3)

    def test_float_profit(self):
        """Прибыль задана числами float"""
        matrix = [[1.5, 2.0], [3.0, 4.5]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 4.5, 1)

    def test_two_optima(self):
        """Два плана с прибылью 7"""
        matrix = [[1, 2, 2], [3, 5, 4], [7, 6, 5]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 7, 2)

    def test_ten_optima(self):
        """Пример из main.py: десять планов с прибылью 3"""
        matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 3, 10)

    def test_lecture_table(self):
        """Таблица с лекции: прибыль 73, один план"""
        matrix = [
            [15, 18, 16, 17],
            [20, 22, 23, 19],
            [26, 28, 27, 25],
            [34, 33, 29, 31],
            [40, 39, 41, 37],
        ]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 73, 1)


if __name__ == "__main__":
    unittest.main()
