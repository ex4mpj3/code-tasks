import unittest

from main import ErrorMessages, ProfitValueError, get_invest_distribution, Result


def _realized_profit(matrix, distribution):
    """Вычисляет фактическую прибыль на основе матрицы и распределения."""
    profit = 0
    for project, lots in enumerate(distribution):
        if lots != 0:
            profit += matrix[lots - 1][project]
    return profit


def _assert_optimal_result(test_case, matrix, result, expected_profit):
    """Проверяет оптимальность результата: прибыль, размерность и сумму лотов."""
    levels = len(matrix)
    projects = len(matrix[0])
    test_case.assertEqual(result.profit, expected_profit)
    test_case.assertEqual(len(result.distribution), projects)
    test_case.assertEqual(sum(result.distribution), levels)
    for lots in result.distribution:
        test_case.assertGreaterEqual(lots, 0)
        test_case.assertLessEqual(lots, levels)
    test_case.assertAlmostEqual(
        _realized_profit(matrix, result.distribution), expected_profit, places=5
    )


class TestInvestDistribution(unittest.TestCase):
    """Набор тестов распределения инвестиций."""

    def test_none(self):
        """Тест с аргументом None."""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution(None)
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_bool_value(self):
        """Тест, когда в клетке bool."""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution([[1, True]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_non_list_in_matrix(self):
        """Тест, когда элемент верхнего уровня не список."""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution([1, 2, 3])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_empty(self):
        """Тест с пустым списком."""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_empty_inner_list(self):
        """Тест со списком, но внутренний список пустой."""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([[]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_jagged_matrix(self):
        """Тест с непрямоугольной матрицей."""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([[1, 2], [3]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_negative_profit(self):
        """Тест с отрицательной прибылью."""
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distribution([[1, -1]])
        self.assertEqual(str(error.exception), ErrorMessages.NEG_PROFIT)
        self.assertEqual(error.exception.project_idx, 1)
        self.assertEqual(error.exception.row_idx, 0)

    def test_decreasing_profit(self):
        """Тест, когда прибыль убывает по столбцу."""
        matrix = [[1, 1, 1], [2, 3, 2], [2, 2, 3]]
        with self.assertRaises(ProfitValueError) as error:
            get_invest_distribution(matrix)
        self.assertEqual(str(error.exception), ErrorMessages.DECR_PROFIT)
        self.assertEqual(error.exception.project_idx, 1)
        self.assertEqual(error.exception.row_idx, 2)

    def test_single(self):
        """Тест с одним проектом и одним уровнем."""
        matrix = [[1]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 1)
        self.assertEqual(result.distribution, [1])

    def test_single_project_multiple_levels(self):
        """Тест с одним проектом и несколькими уровнями."""
        matrix = [[10], [20], [25]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 25)
        self.assertEqual(result.distribution, [3])

    def test_multiple_projects_single_level(self):
        """Тест с несколькими проектами и одним уровнем."""
        matrix = [[10, 5, 12]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 12)
        self.assertEqual(sum(result.distribution), 1)
        self.assertIn(result.distribution, [[0, 0, 1], [1, 0, 0]])

    def test_float_profit(self):
        """Тест, когда прибыль задана числами float."""
        matrix = [[1.5, 2.0], [3.0, 4.5]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 4.5)

    def test_lecture_table(self):
        """Тест с таблицей из лекции: ожидаемая прибыль 73."""
        matrix = [
            [15, 18, 16, 17],
            [20, 22, 23, 19],
            [26, 28, 27, 25],
            [34, 33, 29, 31],
            [40, 39, 41, 37],
        ]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 73)

    def test_zero_profits(self):
        """Тест, когда все прибыли равны нулю."""
        matrix = [[0, 0], [0, 0]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 0)
        self.assertEqual(sum(result.distribution), 2)

    def test_different_optimal_distributions(self):
        """Тест, когда есть несколько оптимальных распределений."""
        matrix = [
            [10, 10],
            [15, 15]
        ]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 15)
        self.assertIn(result.distribution, [[2, 0], [0, 2]])

    def test_all_zeros_matrix(self):
        """Тест с матрицей, где все значения 0."""
        matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 0)
        self.assertEqual(sum(result.distribution), 3)

    def test_strictly_increasing_profit(self):
        """Тест со строго возрастающей прибылью."""
        matrix = [
            [10, 11],
            [20, 22],
            [30, 33]
        ]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 33)
        self.assertEqual(result.distribution, [0, 3])

    def test_non_integer_values_in_matrix(self):
        """Тест с нечисловыми значениями в матрице."""
        with self.assertRaises(TypeError) as error:
            get_invest_distribution([[1, "abc"]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

        with self.assertRaises(TypeError) as error:
            get_invest_distribution([[{"key": "value"}]])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)


if __name__ == "__main__":
    unittest.main()