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

    def test_example_from_main(self):
        """Пример из main.py"""
        weights = [11, 4, 8, 6, 3, 5, 5]
        costs = [17, 6, 11, 10, 5, 8, 6]
        weight_limit = 30
        result = DynamicSolver(weights, costs, weight_limit).get_knapsack()
        self.assertEqual(result.cost, 46)
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


if __name__ == "__main__":
    unittest.main()
