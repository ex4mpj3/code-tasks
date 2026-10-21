import unittest
from itertools import combinations_with_replacement, product

from main import ErrorMessages, ProfitValueError, Result, get_invest_distributions


def _realized_profit(matrix, distribution):
    profit = 0
    for project, lots in enumerate(distribution):
        if lots != 0:
            profit += matrix[lots - 1][project]
    return profit


def _assert_all_optima(
    test_case, matrix, result, expected_profit, expected_count, expected_plans=None
):
    levels = len(matrix)
    projects = len(matrix[0])
    test_case.assertIsInstance(result, Result)
    test_case.assertIsInstance(result.distributions, list)
    test_case.assertEqual(result.profit, expected_profit)
    test_case.assertEqual(len(result.distributions), expected_count)
    seen = []
    for distribution in result.distributions:
        test_case.assertEqual(len(distribution), projects)
        test_case.assertEqual(sum(distribution), levels)
        for lots in distribution:
            test_case.assertIsInstance(lots, int)
            test_case.assertNotIsInstance(lots, bool)
            test_case.assertGreaterEqual(lots, 0)
            test_case.assertLessEqual(lots, levels)
        test_case.assertEqual(_realized_profit(matrix, distribution), expected_profit)
        key = tuple(distribution)
        test_case.assertNotIn(key, seen)
        seen.append(key)
    if expected_plans is not None:
        test_case.assertEqual(set(seen), expected_plans)


def _assert_error(test_case, matrix, error_type, message):
    with test_case.assertRaises(error_type) as error:
        get_invest_distributions(matrix)
    test_case.assertEqual(str(error.exception), message)


def _assert_profit_error(test_case, matrix, message, project, row):
    with test_case.assertRaises(ProfitValueError) as error:
        get_invest_distributions(matrix)
    test_case.assertEqual(str(error.exception), message)
    test_case.assertEqual(error.exception.project_idx, project)
    test_case.assertEqual(error.exception.row_idx, row)


def _brute_force_optima(matrix):
    """Независимый эталон для маленьких таблиц: перебор всех планов"""
    levels = len(matrix)
    projects = len(matrix[0])
    best_profit = -1
    best_plans = set()
    for plan in product(range(levels + 1), repeat=projects):
        if sum(plan) != levels:
            continue
        profit = _realized_profit(matrix, plan)
        if profit > best_profit:
            best_profit = profit
            best_plans = {plan}
        elif profit == best_profit:
            best_plans.add(plan)
    return best_profit, best_plans


def _small_monotone_tables():
    for levels, projects, max_profit in ((3, 2, 3), (2, 3, 2)):
        columns = list(combinations_with_replacement(range(max_profit + 1), levels))
        for selected_columns in product(columns, repeat=projects):
            yield [list(row) for row in zip(*selected_columns)]


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

    def test_empty(self):
        """Пустой список"""
        with self.assertRaises(ValueError) as error:
            get_invest_distributions([])
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

    def test_invalid_table_types(self):
        """Таблица и каждая её строка должны быть списками"""
        for matrix in (42, 1.5, True, "12", {}, (), ((1, 2),), [1, 2], [(1, 2)]):
            with self.subTest(matrix=matrix):
                _assert_error(self, matrix, TypeError, ErrorMessages.TABLE_NOT_NUMBERS)

    def test_invalid_cell_types(self):
        """Строки, None, bool, complex, NaN и контейнеры не являются прибылью"""
        for cell in ("2", None, True, False, 2 + 0j, float("nan"), [], {}):
            with self.subTest(cell=cell):
                matrix = [[1, 1], [2, cell]]
                _assert_error(self, matrix, TypeError, ErrorMessages.TABLE_NOT_NUMBERS)

    def test_empty_rows_and_ragged_tables(self):
        """Пустые строки и строки разной длины"""
        for matrix in (
            [[]],
            [[], []],
            [[1], [2, 3]],
            [[1, 2], [3]],
            [[1], []],
            [[1], [2], [3, 4]],
        ):
            with self.subTest(matrix=matrix):
                _assert_error(self, matrix, ValueError, ErrorMessages.TABLE_NOT_RECT)

    def test_negative_profit_coordinates(self):
        """Отрицательная клетка: разные строки, столбцы и числовые типы"""
        cases = (
            ([[-1, 0]], 0, 0),
            ([[0], [-0.5]], 0, 1),
            ([[0, 0, -0.25]], 2, 0),
        )
        for matrix, project, row in cases:
            with self.subTest(matrix=matrix):
                _assert_profit_error(
                    self, matrix, ErrorMessages.NEG_PROFIT, project, row
                )

    def test_decreasing_profit_coordinates(self):
        """Убывание прибыли в разных строках и столбцах"""
        cases = (
            ([[2, 1], [1, 2]], 0, 1),
            ([[0, 1.5], [1, 1.25]], 1, 1),
            ([[1], [2], [2], [1]], 0, 3),
        )
        for matrix, project, row in cases:
            with self.subTest(matrix=matrix):
                _assert_profit_error(
                    self, matrix, ErrorMessages.DECR_PROFIT, project, row
                )

    def test_one_project_uses_all_lots(self):
        """Все лоты получает единственный проект"""
        matrix = [[0], [2], [2], [7]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 7, 1, {(4,)})

    def test_one_lot_unique_best_project(self):
        """Один лот и единственный лучший проект"""
        matrix = [[1, 3, 2, 0]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 3, 1, {(0, 1, 0, 0)})

    def test_one_lot_tied_best_projects(self):
        """Один лот и несколько равноприбыльных лучших проектов"""
        matrix = [[3, 0, 3, 3]]
        result = get_invest_distributions(matrix)
        expected_plans = {(1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)}
        _assert_all_optima(self, matrix, result, 3, 3, expected_plans)

    def test_zero_profit_all_plans_are_optimal(self):
        """При нулевой прибыли оптимальны все распределения"""
        matrix = [[0, 0, 0], [0, 0, 0]]
        result = get_invest_distributions(matrix)
        expected_plans = {
            (2, 0, 0),
            (0, 2, 0),
            (0, 0, 2),
            (1, 1, 0),
            (1, 0, 1),
            (0, 1, 1),
        }
        _assert_all_optima(self, matrix, result, 0, 6, expected_plans)

    def test_plateau_still_requires_all_lots(self):
        """При постоянной прибыли всё равно нужно распределить все лоты"""
        matrix = [[5, 5], [5, 5], [5, 5], [5, 5]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 10, 3, {(1, 3), (2, 2), (3, 1)})

    def test_concentrating_lots_can_be_optimal(self):
        """Максимум достигается вложением всех лотов в один проект"""
        matrix = [[1, 2], [2, 3], [9, 4]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 9, 1, {(3, 0)})

    def test_splitting_lots_can_be_optimal(self):
        """Максимум достигается распределением лотов между всеми проектами"""
        matrix = [[5, 4, 3], [6, 5, 4], [7, 6, 5]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 12, 1, {(1, 1, 1)})

    def test_unused_middle_project(self):
        """Проект в середине таблицы не получает лотов"""
        matrix = [[5, 0, 4], [6, 0, 5], [7, 0, 6]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 10, 2, {(1, 0, 2), (2, 0, 1)})

    def test_ties_at_multiple_intermediate_steps(self):
        """Один конечный выбор содержит несколько оптимальных префиксов"""
        matrix = [[1, 1, 0], [2, 2, 0], [3, 3, 10], [4, 4, 10]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 11, 2, {(1, 0, 3), (0, 1, 3)})

    def test_mixed_int_and_float_with_ties(self):
        """Таблица из int и float с несколькими оптимальными планами"""
        matrix = [[0.5, 1], [1, 1.5], [2.0, 2]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 2, 4, {(3, 0), (2, 1), (1, 2), (0, 3)})

    def test_close_float_profits_are_not_equal(self):
        """Близкие значения float не считаются равными"""
        matrix = [[1.0, 1.0 + 2**-40]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, 1.0 + 2**-40, 1, {(0, 1)})

    def test_large_integer_profit_stays_exact(self):
        """Большие целые значения прибыли сравниваются без потери точности"""
        value = 2**60
        matrix = [[value, value + 1]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, value + 1, 1, {(0, 1)})

    def test_integer_profit_beyond_float_range(self):
        """Целые больше предела float считаются точно и без ошибок"""
        value = 10**400
        matrix = [[value, 1], [value, 2]]
        result = get_invest_distributions(matrix)
        _assert_all_optima(self, matrix, result, value + 1, 1, {(1, 1)})

    def test_small_tables_against_exhaustive_search(self):
        """Все 616 монотонных таблиц двух небольших размеров"""
        for matrix in _small_monotone_tables():
            with self.subTest(matrix=matrix):
                profit, plans = _brute_force_optima(matrix)
                result = get_invest_distributions(matrix)
                _assert_all_optima(self, matrix, result, profit, len(plans), plans)

    def test_large_table_linear_profit(self):
        """Таблица 50x50: все лоты выгоднее отдать последнему проекту"""
        matrix = [[lots * rate for rate in range(1, 51)] for lots in range(1, 51)]
        result = get_invest_distributions(matrix)
        expected_plan = (0,) * 49 + (50,)
        _assert_all_optima(self, matrix, result, 2500, 1, {expected_plan})


if __name__ == "__main__":
    unittest.main()
