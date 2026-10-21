import unittest

from main import (
    CELL_NOT_NUMBER,
    TABLE_NOT_LISTS,
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
    test_case.assertIsNotNone(price_table[0][0])
    test_case.assertIsNotNone(price_table[height - 1][width - 1])
    for previous, current in zip(result.path, result.path[1:]):
        test_case.assertTrue(_is_allowed_step(previous, current))
        test_case.assertIsNotNone(price_table[current[0]][current[1]])
    test_case.assertEqual(_path_sum(price_table, result.path), expected_cost)


class TestMinCostPath(unittest.TestCase):
    """Набор тестов пути минимальной стоимости"""

    def test_none_argument(self):
        """Аргумент None — нет таблицы"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path(None)
        self.assertEqual(str(error.exception), TABLE_NOT_LISTS)

    def test_str_value(self):
        """В клетке строка"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, "ab"]])
        self.assertEqual(str(error.exception), CELL_NOT_NUMBER)

    def test_bool_value(self):
        """В клетке bool"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, True]])
        self.assertEqual(str(error.exception), CELL_NOT_NUMBER)

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

    def test_single_none(self):
        """Единственная клетка запрещена"""
        self.assertEqual(get_min_cost_path([[None]]), Result(None, None))

    def test_double(self):
        """Таблица 2 на 2"""
        table = [[1.1, 2], [3, 4]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=7.1, path=[(0, 0), (0, 1), (1, 1)]),
        )

    def test_double_with_none(self):
        """Таблица 2 на 2 со стеной"""
        table = [[1.1, None], [3, 4]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=8.1, path=[(0, 0), (1, 0), (1, 1)]),
        )

    def test_triple_no_path(self):
        """Стены отрезают финиш"""
        table = [[1, None, 2], [None, 4, 2], [1, 1, 2]]
        self.assertEqual(get_min_cost_path(table), Result(None, None))

    def test_rectangle_with_none(self):
        """Прямоугольная таблица 2 на 3 со стенами"""
        table = [[1, None, None], [3, 4, 1]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=9, path=[(0, 0), (1, 0), (1, 1), (1, 2)]),
        )

    def test_tuple_argument(self):
        """Аргумент не является списком"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path(([1, 2],)) # type: ignore
        self.assertEqual(str(error.exception), TABLE_NOT_LISTS)

    def test_non_list_row(self):
        """Строка таблицы не является списком"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, 2], (3, 4)]) # type: ignore
        self.assertEqual(str(error.exception), TABLE_NOT_LISTS)

    def test_object_value(self):
        """В клетке объект неподдерживаемого типа"""
        with self.assertRaises(TypeError) as error:
            get_min_cost_path([[1, object()]]) # type: ignore
        self.assertEqual(str(error.exception), CELL_NOT_NUMBER)

    def test_empty_row(self):
        """Таблица содержит пустую строку"""
        with self.assertRaises(ValueError) as error:
            get_min_cost_path([[]])
        self.assertEqual(str(error.exception), TABLE_NOT_RECT)

    def test_blocked_start(self):
        """Стартовая клетка запрещена"""
        table = [[None, 1], [2, 3]]
        self.assertEqual(get_min_cost_path(table), Result(None, None))

    def test_blocked_finish(self):
        """Финишная клетка запрещена"""
        table = [[1, 2], [3, None]]
        self.assertEqual(get_min_cost_path(table), Result(None, None))

    def test_single_row(self):
        """Путь проходит по одной строке"""
        table = [[2, 1, 3]]
        self.assertEqual(
            get_min_cost_path(table),
            Result(cost=6, path=[(0, 0), (0, 1), (0, 2)]),
        )

    def test_single_row_no_path(self):
        """Запрещённая клетка отрезает путь в одной строке"""
        table = [[2, None, 3]]
        self.assertEqual(get_min_cost_path(table), Result(None, None))

    def test_single_column(self):
        """Путь проходит по одному столбцу"""
        table = [[2], [1], [3]]
        self.assertEqual(
            get_min_cost_path(table), # type: ignore
            Result(cost=6, path=[(0, 0), (1, 0), (2, 0)]),
        )

    def test_negative_costs(self):
        """В таблице есть отрицательные стоимости"""
        table = [[1, -5, 2], [2, 1, 1]]
        result = get_min_cost_path(table) # type: ignore
        _assert_optimal_result(self, table, result, expected_cost=-2)

    def test_multiple_optimal_paths(self):
        """Несколько путей имеют одинаковую минимальную стоимость"""
        table = [[1, 1], [1, 1]]
        result = get_min_cost_path(table) # type: ignore
        _assert_optimal_result(self, table, result, expected_cost=3)

    def test_float_values(self):
        """В таблице используются вещественные числа"""
        table = [[0.5, 1.25], [2.0, 0.25]]
        result = get_min_cost_path(table) # type: ignore
        _assert_optimal_result(self, table, result, expected_cost=2.0)


if __name__ == "__main__":
    unittest.main()
