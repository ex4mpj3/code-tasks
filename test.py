import unittest

from main import (
    TABLE_NOT_NUMBERS,
    TABLE_NOT_RECT,
    Result,
    get_min_cost_path,
)


def _path_sum(price_table, path):
    return sum(price_table[row][column] for row, column in path)


def _is_allowed_step(previous, current):
    row_delta = current[0] - previous[0]
    column_delta = current[1] - previous[1]
    return (row_delta, column_delta) in {(1, 0), (0, 1)}


def _assert_optimal_result(test_case, price_table, result, expected_cost):
    height = len(price_table)
    width = len(price_table[0])
    test_case.assertEqual(result.cost, expected_cost)
    test_case.assertIsInstance(result.path, list)
    test_case.assertGreaterEqual(len(result.path), 1)
    test_case.assertEqual(result.path[0], (0, 0))
    test_case.assertEqual(result.path[-1], (height - 1, width - 1))
    for previous, current in zip(result.path, result.path[1:]):
        test_case.assertTrue(_is_allowed_step(previous, current))
    test_case.assertEqual(_path_sum(price_table, result.path), expected_cost)


class TestMinCostPath(unittest.TestCase):
    """Набор тестов пути минимальной стоимости"""

    def test_none(self):
        """Аргумент None"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path(None)
        self.assertEqual(str(error.exception), TABLE_NOT_NUMBERS)

    def test_str_value(self):
        """В клетке строка"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, "ab"]])
        self.assertEqual(str(error.exception), TABLE_NOT_NUMBERS)

    def test_bool_value(self):
        """В клетке bool"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, True]])
        self.assertEqual(str(error.exception), TABLE_NOT_NUMBERS)

    def test_empty(self):
        """Пустой список"""
        with self.assertRaises(ValueError) as error:
            get_min_cost_path([])
        self.assertEqual(str(error.exception), TABLE_NOT_RECT)

    def test_jagged(self):
        """Строки разной длины"""
        with self.assertRaises(ValueError) as error:
            get_min_cost_path([[1.0, 2.0, 3.0], [1.0, 2.0]])
        self.assertEqual(str(error.exception), TABLE_NOT_RECT)

    def test_single(self):
        """Таблица 1 на 1"""
        self.assertEqual(get_min_cost_path([[1]]), Result(cost=1, path=[(0, 0)]))

    def test_double(self):
        """Таблица 2 на 2"""
        table = [[1.1, 2], [3, 4]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=7.1, path=[(0, 0), (0, 1), (1, 1)]),
        )

    def test_triple(self):
        """Таблица 3 на 3"""
        table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(
                cost=8,
                path=[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
            ),
        )

    def test_rectangle(self):
        """Прямоугольная таблица 2 на 3"""
        table = [[1, 2, 2], [3, 4, 1]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=6, path=[(0, 0), (0, 1), (0, 2), (1, 2)]),
        )

    def test_single_row(self):
        """Таблица из одной строки"""
        table = [[1, 3, 2, 4]]
        _assert_optimal_result(self, table, get_min_cost_path(table), 10)

    def test_single_column(self):
        """Таблица из одного столбца"""
        table = [[2], [3], [1], [4]]
        _assert_optimal_result(self, table, get_min_cost_path(table), 10)

    def test_zero_values(self):
        """Таблица с нулями"""
        table = [[0, 0, 0], [0, 0, 0]]
        _assert_optimal_result(self, table, get_min_cost_path(table), 0)

    def test_negative_values(self):
        """Отрицательные стоимости клеток"""
        table = [[2, -5], [4, -3]]
        _assert_optimal_result(self, table, get_min_cost_path(table), -6)

    def test_float_values(self):
        """Дробные стоимости клеток"""
        table = [[1.5, 0.5], [2.5, 1.25]]
        _assert_optimal_result(self, table, get_min_cost_path(table), 3.25)

    def test_equal_paths(self):
        """Несколько путей с одинаковой стоимостью"""
        table = [[1, 1], [1, 1]]
        _assert_optimal_result(self, table, get_min_cost_path(table), 3)

    def test_not_greedy(self):
        """Проверка выбора минимального пути целиком"""
        table = [[1, 1, 99], [2, 100, 99], [3, 1, 1]]
        _assert_optimal_result(self, table, get_min_cost_path(table), 8)

    def test_large_rectangle(self):
        """Прямоугольная таблица 2 на 4"""
        table = [[1, 1, 100, 1], [9, 1, 1, 1]]
        _assert_optimal_result(self, table, get_min_cost_path(table), 5)

    def test_empty_rows(self):
        """Таблица с пустыми строками"""
        for table in ([[]], [[], []]):
            with self.subTest(table=table):
                with self.assertRaises(ValueError):
                    get_min_cost_path(table)

    def test_invalid_table(self):
        """Вместо таблицы передан другой тип"""
        for table in (123, "123", ([1, 2], [3, 4])):
            with self.subTest(table=table):
                with self.assertRaises(TypeError):
                    get_min_cost_path(table)

    def test_invalid_rows(self):
        """Строки таблицы не являются списками"""
        for table in ([1, 2], [[1, 2], (3, 4)]):
            with self.subTest(table=table):
                with self.assertRaises(TypeError):
                    get_min_cost_path(table)

    def test_invalid_cell_values(self):
        """Другие недопустимые типы клеток"""
        for value in (None, False, 2 + 3j, [5]):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    get_min_cost_path([[1, value]])


if __name__ == "__main__":
    unittest.main()
