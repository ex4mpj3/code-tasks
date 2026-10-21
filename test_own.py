import unittest

from main import ErrorMessages, ProfitValueError, get_invest_distribution


def _realized_profit(matrix, distribution):
    """Вычисляет реализованную прибыль по матрице и распределению."""
    profit = 0
    for project, lots in enumerate(distribution):
        if lots != 0:
            profit += matrix[lots - 1][project]
    return profit


def _assert_optimal_result(test_case, matrix, result, expected_profit):
    """Проверяет корректность оптимального результата."""
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


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев."""

    def test_very_small_float_values(self):
        """Проверка работы с очень маленькими значениями float."""
        matrix = [[0.001, 0.002], [0.003, 0.004]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 0.004)

    def test_large_integer_values(self):
        """Проверка работы с большими целыми числами."""
        matrix = [[1000000, 2000000], [3000000, 4000000]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 4000000)

    def test_single_row_with_many_projects(self):
        """Проверка одной строки с множеством проектов."""
        matrix = [[i for i in range(1, 11)]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 10)

    def test_single_column_with_many_levels(self):
        """Проверка одного столбца с множеством уровней."""
        matrix = [[i] for i in range(1, 11)]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 10)

    def test_all_same_values(self):
        """Проверка матрицы с одинаковыми значениями."""
        matrix = [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 15)  # ← Исправлено: 5+5+5=15


class TestResultStructure(unittest.TestCase):
    """Тесты структуры результата."""

    def test_result_has_profit_field(self):
        """Проверка наличия поля profit в результате."""
        result = get_invest_distribution([[1]])
        self.assertTrue(hasattr(result, "profit"))

    def test_result_has_distribution_field(self):
        """Проверка наличия поля distribution в результате."""
        result = get_invest_distribution([[1]])
        self.assertTrue(hasattr(result, "distribution"))

    def test_distribution_is_list(self):
        """Проверка, что distribution является списком."""
        result = get_invest_distribution([[1, 2], [3, 4]])
        self.assertIsInstance(result.distribution, list)

    def test_profit_is_number(self):
        """Проверка, что profit является числом."""
        result = get_invest_distribution([[1, 2], [3, 4]])
        self.assertIsInstance(result.profit, (int, float))

    def test_distribution_length_equals_projects(self):
        """Проверка, что длина distribution равна числу проектов."""
        matrix = [[1, 2, 3, 4], [5, 6, 7, 8]]
        result = get_invest_distribution(matrix)
        self.assertEqual(len(result.distribution), 4)


if __name__ == "__main__":
    unittest.main()