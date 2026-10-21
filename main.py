import math
from collections import namedtuple
from enum import StrEnum

UNREACHABLE = float("-inf")


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках"""

    TABLE_NOT_NUMBERS = "Таблица прибыли не является списком списков чисел"
    TABLE_NOT_RECT = "Таблица прибыли не является прямоугольной матрицей"
    NEG_PROFIT = "Значение прибыли не может быть отрицательно"
    DECR_PROFIT = "Значение прибыли не может убывать с ростом инвестиций"


Result = namedtuple("Result", ["profit", "distributions"])


class ProfitValueError(Exception):
    def __init__(self, message: str, project_idx: int, row_idx: int) -> None:
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)


def get_invest_distributions(
    profit_matrix: list[list[float | int]],
) -> Result:
    """Возвращает максимальную прибыль и все распределения всех лотов

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distributions
    """
    validate_profit_matrix(profit_matrix)
    lots_count = len(profit_matrix)
    max_profits = [0] + [UNREACHABLE] * lots_count
    best_lots = []
    for project_idx in range(len(profit_matrix[0])):
        project_profits = [0] + [row[project_idx] for row in profit_matrix]
        max_profits, project_best_lots = add_project(max_profits, project_profits)
        best_lots.append(project_best_lots)
    distributions = collect_distributions(best_lots, lots_count)
    return Result(max_profits[lots_count], distributions)


def add_project(
    previous_profits: list[float | int], project_profits: list[float | int]
) -> tuple[list[float | int], list[list[int]]]:
    max_profits = []
    best_lots = []
    for j in range(len(previous_profits)):
        candidates = {
            x: previous_profits[j - x] + project_profits[x]
            for x in range(j + 1)
            if previous_profits[j - x] != UNREACHABLE
        }
        max_profit = max(candidates.values())
        max_profits.append(max_profit)
        best_lots.append([x for x in candidates if candidates[x] == max_profit])
    return max_profits, best_lots


def collect_distributions(
    best_lots: list[list[list[int]]], lots_count: int
) -> list[list[int]]:
    distributions = [[]]
    for project_best_lots in reversed(best_lots):
        distributions = [
            [x] + distribution
            for distribution in distributions
            for x in project_best_lots[lots_count - sum(distribution)]
        ]
    return distributions


def validate_profit_matrix(profit_matrix: list[list[float | int]]) -> None:
    if not is_number_table(profit_matrix):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    if not profit_matrix or not profit_matrix[0]:
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)
    if any(len(row) != len(profit_matrix[0]) for row in profit_matrix):
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)
    validate_profit_values(profit_matrix)


def is_number_table(profit_matrix: object) -> bool:
    return isinstance(profit_matrix, list) and all(
        isinstance(row, list) and all(is_number(cell) for cell in row)
        for row in profit_matrix
    )


def is_number(cell: object) -> bool:
    if isinstance(cell, float):
        return not math.isnan(cell)
    return isinstance(cell, int) and not isinstance(cell, bool)


def validate_profit_values(profit_matrix: list[list[float | int]]) -> None:
    for row_idx in range(len(profit_matrix)):
        for project_idx in range(len(profit_matrix[0])):
            validate_profit(profit_matrix, row_idx, project_idx)


def validate_profit(
    profit_matrix: list[list[float | int]], row_idx: int, project_idx: int
) -> None:
    profit = profit_matrix[row_idx][project_idx]
    if profit < 0:
        raise ProfitValueError(ErrorMessages.NEG_PROFIT, project_idx, row_idx)
    if row_idx > 0 and profit < profit_matrix[row_idx - 1][project_idx]:
        raise ProfitValueError(ErrorMessages.DECR_PROFIT, project_idx, row_idx)


def main():
    profit_matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    print(get_invest_distributions(profit_matrix))


if __name__ == "__main__":
    main()
