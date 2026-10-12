"""Пример использования DynamicSolver.

Класс DynamicSolver нужно реализовать в dynamic_solver.py.
Методы get_weight, get_cost и _validate_params — в knapsack_abs_solver.py.
"""

from dynamic_solver import DynamicSolver


def main():
    weights = [11, 4, 8, 6, 3, 5, 5]
    costs = [17, 6, 11, 10, 5, 8, 6]
    weight_limit = 30
    print("Пример решения задачи о рюкзаке динамическим программированием")
    print(f"Веса предметов: {weights}")
    print(f"Стоимости предметов: {costs}")
    print(f"Ограничение вместимости: {weight_limit}")
    solver = DynamicSolver(weights, costs, weight_limit)
    result = solver.get_knapsack()
    print(f"Максимальная стоимость: {result.cost}, индексы предметов: {result.items}")


if __name__ == "__main__":
    main()
