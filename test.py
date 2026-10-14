import unittest

from dynamic_solver import DynamicSolver
from knapsack_abs_solver import (
    COSTS,
    EMPTY_LIST,
    LENGTHS_NOT_EQUAL,
    LESS_WEIGHT_LIMIT,
    NOT_INT,
    NOT_INT_WEIGHT_LIMIT,
    NOT_LIST,
    NOT_POS,
    NOT_POS_WEIGHT_LIMIT,
    WEIGHTS,
)


def check_knapsack_items(weights, costs, weight_limit, result) -> bool:
    """Проверяет, что набор укладывается в вместимость и стоимость совпадает"""
    items_cnt = len(weights)
    cost = result.cost
    items = result.items
    if len(items) > items_cnt or len(items) == 0:
        return False
    if len(set(items)) != len(items):
        return False
    sum_cost = 0
    sum_weight = 0
    for idx in items:
        if idx < 0 or idx >= items_cnt:
            return False
        sum_cost += costs[idx]
        sum_weight += weights[idx]
    if sum_weight > weight_limit:
        return False
    return sum_cost == cost


class TestDynamicSolver(unittest.TestCase):
    """Набор тестов рюкзака динамическим программированием"""

    def test_2(self):
        """Два предмета"""
        weights = [1, 1]
        costs = [1, 2]
        weight_limit = 1
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 2)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_3(self):
        """Три предмета"""
        weights = [1, 1, 2]
        costs = [1, 2, 2]
        weight_limit = 2
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 3)
        self.assertTrue(check_knapsack_items(weights, costs, weight_limit, result))

    def test_not_list_weights(self):
        """Веса не список"""
        with self.assertRaises(TypeError) as error:
            DynamicSolver(1, [1, 1], 1)
        self.assertEqual(NOT_LIST.format(WEIGHTS), str(error.exception))

    def test_not_list_costs(self):
        """Стоимости не список"""
        with self.assertRaises(TypeError) as error:
            DynamicSolver([1], "str", 1)
        self.assertEqual(NOT_LIST.format(COSTS), str(error.exception))

    def test_one_item(self):
        """Один предмет, который помещается"""
        result = DynamicSolver([5], [7], 5).get_knapsack()
        self.assertEqual(result.cost, 7)
        self.assertEqual(result.items, [0])

    def test_all_items_fit(self):
        """Все предметы помещаются — берём все"""
        weights = [2, 3, 4]
        costs = [5, 1, 7]
        result = DynamicSolver(weights, costs, 100).get_knapsack()
        self.assertEqual(result.cost, 13)
        self.assertCountEqual(result.items, [0, 1, 2])

    def test_heavy_item_skipped(self):
        """Предмет тяжелее вместимости не берётся"""
        weights = [10, 2]
        costs = [100, 1]
        result = DynamicSolver(weights, costs, 5).get_knapsack()
        self.assertEqual(result.cost, 1)
        self.assertEqual(result.items, [1])

    def test_greedy_is_wrong(self):
        """Самый дорогой предмет брать невыгодно"""
        weights = [6, 3, 3]
        costs = [10, 6, 6]
        result = DynamicSolver(weights, costs, 6).get_knapsack()
        self.assertEqual(result.cost, 12)
        self.assertCountEqual(result.items, [1, 2])

    def test_known_cases(self):
        """Известные ответы"""
        cases = [
            ([3, 4, 5], [4, 5, 6], 7, 9),
            ([1, 3, 4, 5], [1, 4, 5, 7], 7, 9),
            ([10, 20, 30], [60, 100, 120], 50, 220),
            ([5, 4, 6, 3], [10, 40, 30, 50], 10, 90),
            ([2, 2, 2, 2], [3, 3, 3, 3], 5, 6),
            ([6, 5, 5], [9, 7, 7], 10, 14),
        ]
        for weights, costs, weight_limit, cost in cases:
            with self.subTest(weights=weights, weight_limit=weight_limit):
                result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
                self.assertEqual(result.cost, cost)
                self.assertTrue(
                    check_knapsack_items(weights, costs, weight_limit, result)
                )

    def test_many_items(self):
        """Много предметов: 60 предметов считаются быстро"""
        weights = [1] * 60
        costs = list(range(1, 61))
        result = DynamicSolver(weights, costs, 10).get_knapsack()
        self.assertEqual(result.cost, 555)
        self.assertCountEqual(result.items, list(range(50, 60)))

    def test_get_weight_and_cost(self):
        """Вес и стоимость набора"""
        solver = DynamicSolver([3, 4, 5], [4, 5, 6], 7)
        cases = [
            ([False, False, False], 0, 0),
            ([True, False, False], 3, 4),
            ([True, True, False], 7, 9),
            ([False, True, True], 9, 0),
            ([True, True, True], 12, 0),
        ]
        for selected_items, weight, cost in cases:
            with self.subTest(selected_items=selected_items):
                self.assertEqual(solver.get_weight(selected_items), weight)
                self.assertEqual(solver.get_cost(selected_items), cost)

    def test_properties(self):
        """Свойства объекта"""
        solver = DynamicSolver([3, 4], [4, 5], 7)
        self.assertEqual(solver.item_cnt, 2)
        self.assertEqual(solver.weights, [3, 4])
        self.assertEqual(solver.costs, [4, 5])
        self.assertEqual(solver.weight_limit, 7)

    def test_not_list(self):
        """Веса или стоимости не список"""
        cases = [
            ((1, 2), [1, 2], WEIGHTS),
            ("12", [1, 2], WEIGHTS),
            (None, [1], WEIGHTS),
            ([1, 2], (1, 2), COSTS),
            ([1], 5, COSTS),
        ]
        for weights, costs, name in cases:
            with self.subTest(weights=weights, costs=costs):
                with self.assertRaises(TypeError) as error:
                    DynamicSolver(weights, costs, 5)
                self.assertEqual(NOT_LIST.format(name), str(error.exception))

    def test_empty_list(self):
        """Пустой список весов или стоимостей"""
        cases = [([], [1], WEIGHTS), ([1], [], COSTS), ([], [], WEIGHTS)]
        for weights, costs, name in cases:
            with self.subTest(weights=weights, costs=costs):
                with self.assertRaises(ValueError) as error:
                    DynamicSolver(weights, costs, 5)
                self.assertEqual(EMPTY_LIST.format(name), str(error.exception))

    def test_not_int_values(self):
        """Нецелое значение в списке"""
        cases = [
            ([1, 2.5], [1, 2], WEIGHTS),
            (["1", 2], [1, 2], WEIGHTS),
            ([True, 2], [1, 2], WEIGHTS),
            ([1, 2], [1, None], COSTS),
            ([1, 2], [1.0, 2], COSTS),
            ([1, 2], [False, 2], COSTS),
        ]
        for weights, costs, name in cases:
            with self.subTest(weights=weights, costs=costs):
                with self.assertRaises(TypeError) as error:
                    DynamicSolver(weights, costs, 5)
                self.assertEqual(NOT_INT.format(name), str(error.exception))

    def test_not_positive_values(self):
        """Нулевое или отрицательное значение в списке"""
        cases = [
            ([0, 2], [1, 2], WEIGHTS),
            ([1, -3], [1, 2], WEIGHTS),
            ([1, 2], [0, 2], COSTS),
            ([1, 2], [1, -1], COSTS),
        ]
        for weights, costs, name in cases:
            with self.subTest(weights=weights, costs=costs):
                with self.assertRaises(ValueError) as error:
                    DynamicSolver(weights, costs, 5)
                self.assertEqual(NOT_POS.format(name), str(error.exception))

    def test_lengths_not_equal(self):
        """Списки разной длины"""
        for weights, costs in [([1, 2], [1]), ([1], [1, 2, 3])]:
            with self.subTest(weights=weights, costs=costs):
                with self.assertRaises(ValueError) as error:
                    DynamicSolver(weights, costs, 5)
                self.assertEqual(LENGTHS_NOT_EQUAL, str(error.exception))

    def test_weight_limit_not_int(self):
        """Вместимость не целое число"""
        for weight_limit in (5.0, "5", None, True, [5]):
            with self.subTest(weight_limit=weight_limit):
                with self.assertRaises(TypeError) as error:
                    DynamicSolver([1, 2], [1, 2], weight_limit)
                self.assertEqual(NOT_INT_WEIGHT_LIMIT, str(error.exception))

    def test_weight_limit_not_positive(self):
        """Вместимость меньше единицы"""
        for weight_limit in (0, -1, -10):
            with self.subTest(weight_limit=weight_limit):
                with self.assertRaises(ValueError) as error:
                    DynamicSolver([1, 2], [1, 2], weight_limit)
                self.assertEqual(NOT_POS_WEIGHT_LIMIT, str(error.exception))

    def test_weight_limit_less_than_min_weight(self):
        """Вместимость меньше минимального веса"""
        for weight_limit in (1, 2):
            with self.subTest(weight_limit=weight_limit):
                with self.assertRaises(ValueError) as error:
                    DynamicSolver([3, 5], [1, 2], weight_limit)
                self.assertEqual(LESS_WEIGHT_LIMIT, str(error.exception))

    def test_errors_order(self):
        """Порядок проверок: сначала веса, потом стоимости, потом вместимость"""
        with self.assertRaises(TypeError) as error:
            DynamicSolver("w", "c", "l")
        self.assertEqual(NOT_LIST.format(WEIGHTS), str(error.exception))
        with self.assertRaises(ValueError) as error:
            DynamicSolver([1, 2], [1], 0)
        self.assertEqual(LENGTHS_NOT_EQUAL, str(error.exception))


if __name__ == "__main__":
    unittest.main()
