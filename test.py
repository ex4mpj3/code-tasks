import unittest
from copy import deepcopy
from itertools import combinations_with_replacement, product

from main import ErrorMessages, ProfitValueError, Result, get_invest_distribution


def _realized_profit(matrix, distribution):
    """Вычисляет прибыль непосредственно по выданному плану."""
    profit = 0
    for project, lots in enumerate(distribution):
        if lots != 0:
            profit += matrix[lots - 1][project]
    return profit


def _assert_optimal_result(test_case, matrix, result, expected_profit):
    """Проверяет тип ответа, полный бюджет и прибыль фактического плана."""
    levels = len(matrix)
    projects = len(matrix[0])
    test_case.assertIsInstance(result, Result)
    test_case.assertEqual(result.profit, expected_profit)
    test_case.assertEqual(len(result.distribution), projects)
    test_case.assertEqual(sum(result.distribution), levels)
    for lots in result.distribution:
        test_case.assertIs(type(lots), int)
        test_case.assertGreaterEqual(lots, 0)
        test_case.assertLessEqual(lots, levels)
    test_case.assertEqual(
        _realized_profit(matrix, result.distribution), expected_profit
    )


def _brute_force_profit(matrix):
    """Перебирает все малые планы без динамического программирования."""
    levels = len(matrix)
    projects = len(matrix[0])
    return max(
        _realized_profit(matrix, plan)
        for plan in product(range(levels + 1), repeat=projects)
        if sum(plan) == levels
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

    def test_invalid_table_types(self):
        """Внешняя таблица и каждая строка должны быть списками."""
        for matrix in (1, True, "table", {"a": 1}, ((1,),), [1], [(1,)], [None]):
            with self.subTest(matrix=matrix):
                with self.assertRaises(TypeError) as error:
                    get_invest_distribution(matrix)
                self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_invalid_cell_types(self):
        """Ни строки, ни None, ни bool и контейнеры не являются прибылью."""
        for value in ("1", None, True, False, [], {}, 1 + 0j):
            with self.subTest(value=value):
                with self.assertRaises(TypeError) as error:
                    get_invest_distribution([[1, 2], [2, value]])
                self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_NUMBERS)

    def test_empty(self):
        """Пустой список"""
        with self.assertRaises(ValueError) as error:
            get_invest_distribution([])
        self.assertEqual(str(error.exception), ErrorMessages.TABLE_NOT_RECT)

    def test_empty_or_unequal_rows(self):
        """Нулевая ширина и строки разной длины отвергаются одинаково."""
        for matrix in ([[]], [[], []], [[1], []], [[1], [2, 3]], [[1, 2], [3]]):
            with self.subTest(matrix=matrix):
                with self.assertRaises(ValueError) as error:
                    get_invest_distribution(matrix)
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

    def test_profit_error_coordinates(self):
        """Ошибки в поздних строках сохраняют нулевые индексы проекта и строки."""
        for matrix, message in (
            ([[1, 2], [3, -0.5]], ErrorMessages.NEG_PROFIT),
            ([[1, 2], [3, 1.5]], ErrorMessages.DECR_PROFIT),
        ):
            with self.subTest(message=message):
                with self.assertRaises(ProfitValueError) as error:
                    get_invest_distribution(matrix)
                self.assertEqual(str(error.exception), message)
                self.assertEqual(error.exception.project_idx, 1)
                self.assertEqual(error.exception.row_idx, 1)

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

    def test_single_project_receives_every_lot(self):
        """При одном проекте весь бюджет должен попасть в него."""
        matrix = [[0], [2], [5], [9]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 9)
        self.assertEqual(result.distribution, [4])

    def test_single_lot_chooses_best_project(self):
        """При одном лоте сравниваются все проекты прямоугольной таблицы."""
        matrix = [[2, 7, 3, 4]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 7)
        self.assertEqual(result.distribution, [0, 1, 0, 0])

    def test_full_budget_with_zero_or_constant_profit(self):
        """Нулевые прибыли и равные максимумы не позволяют потерять лоты."""
        for matrix in ([[0, 0], [0, 0], [0, 0]], [[2, 2], [2, 2], [2, 2]]):
            with self.subTest(matrix=matrix):
                result = get_invest_distribution(matrix)
                _assert_optimal_result(
                    self, matrix, result, _brute_force_profit(matrix)
                )

    def test_optimum_splits_budget(self):
        """Оптимум может требовать вклада в несколько проектов, а не один."""
        matrix = [[4, 3], [5, 7], [6, 8]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 11)
        self.assertEqual(result.distribution, [1, 2])

    def test_optimum_can_skip_first_or_last_project(self):
        """Неиспользуемые проекты сохраняются в плане как нули."""
        for matrix, expected_plan in (
            ([[0, 2, 1], [0, 8, 2]], [0, 2, 0]),
            ([[2, 1, 0], [8, 2, 0]], [2, 0, 0]),
        ):
            with self.subTest(matrix=matrix):
                result = get_invest_distribution(matrix)
                _assert_optimal_result(self, matrix, result, 8)
                self.assertEqual(result.distribution, expected_plan)

    def test_mixed_int_float_profit(self):
        """Смешанные целые и дробные прибыли сохраняют дробный оптимум."""
        matrix = [[1.5, 2], [2, 2.5], [2.5, 3]]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 4)

    def test_large_integer_profit_stays_exact(self):
        """Целая прибыль не теряет точность при больших значениях."""
        large_profit = 10**100
        matrix = [
            [large_profit, 0],
            [large_profit + 1, large_profit],
            [large_profit + 2, large_profit + 1],
        ]
        result = get_invest_distribution(matrix)
        _assert_optimal_result(self, matrix, result, 2 * large_profit)

    def test_input_is_not_modified(self):
        """Расчёт и повторный вызов не изменяют исходную таблицу."""
        matrix = [[3, 2], [4, 5], [8, 6]]
        original = deepcopy(matrix)
        for _ in range(2):
            result = get_invest_distribution(matrix)
            _assert_optimal_result(self, matrix, result, 8)
            self.assertEqual(matrix, original)

    def test_small_monotone_tables_against_exhaustive_search(self):
        """Все малые неубывающие таблицы сверяются с полным перебором планов."""
        for levels in range(1, 4):
            columns = tuple(combinations_with_replacement(range(3), levels))
            for projects in range(1, 4):
                for table_columns in product(columns, repeat=projects):
                    matrix = [list(row) for row in zip(*table_columns, strict=True)]
                    with self.subTest(matrix=matrix):
                        result = get_invest_distribution(matrix)
                        _assert_optimal_result(
                            self, matrix, result, _brute_force_profit(matrix)
                        )

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
