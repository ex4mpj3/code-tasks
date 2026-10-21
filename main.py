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


def _is_valid_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_table_types(profit_matrix: object) -> None:
    if not isinstance(profit_matrix, list):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)

    for level_row in profit_matrix:
        if not isinstance(level_row, list):
            raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
        for cell_value in level_row:
            if not _is_valid_number(cell_value):
                raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)


def _validate_table_shape(profit_matrix: list[list[float | int]]) -> None:
    if not profit_matrix or not profit_matrix[0]:
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)

    projects_count = len(profit_matrix[0])
    for level_row in profit_matrix:
        if len(level_row) != projects_count:
            raise ValueError(ErrorMessages.TABLE_NOT_RECT)


def _validate_profit_values(profit_matrix: list[list[float | int]]) -> None:
    for row_idx, level_row in enumerate(profit_matrix):
        for project_idx, profit in enumerate(level_row):
            if profit < 0:
                msg = ErrorMessages.NEG_PROFIT
                raise ProfitValueError(msg, project_idx, row_idx)

    for row_idx in range(1, len(profit_matrix)):
        for project_idx, profit in enumerate(profit_matrix[row_idx]):
            prev_level_profit = profit_matrix[row_idx - 1][project_idx]
            if profit < prev_level_profit:
                msg = ErrorMessages.DECR_PROFIT
                raise ProfitValueError(msg, project_idx, row_idx)


def _get_project_profit(
    profit_matrix: list[list[float | int]],
    project_idx: int,
    lots: int,
) -> float | int:
    if lots == 0:
        return 0
    return profit_matrix[lots - 1][project_idx]


def _calculate_max_profits(
    profit_matrix: list[list[float | int]],
) -> list[list[float | int]]:
    total_lots = len(profit_matrix)
    projects_count = len(profit_matrix[0])

    max_profits: list[list[float | int]] = [
        [UNREACHABLE] * (total_lots + 1) for _ in range(projects_count + 1)
    ]
    max_profits[0][0] = 0

    for project_num in range(1, projects_count + 1):
        project_idx = project_num - 1
        for allocated_lots in range(total_lots + 1):
            best_profit: float | int = UNREACHABLE
            for cur_project_lots in range(allocated_lots + 1):
                prev_project_lots = allocated_lots - cur_project_lots
                prev_profit = max_profits[project_num - 1][prev_project_lots]
                cur_project_profit = _get_project_profit(
                    profit_matrix, project_idx, cur_project_lots
                )
                candidate_profit = prev_profit + cur_project_profit
                if candidate_profit > best_profit:
                    best_profit = candidate_profit
            max_profits[project_num][allocated_lots] = best_profit

    return max_profits


def _restore_distributions(
    profit_matrix: list[list[float | int]],
    max_profits: list[list[float | int]],
) -> list[list[int]]:
    total_lots = len(profit_matrix)
    projects_count = len(profit_matrix[0])
    distributions: list[list[int]] = []

    stack: list[tuple[int, int, list[int]]] = [
        (projects_count, total_lots, [0] * projects_count)
    ]

    while stack:
        project_num, remaining_lots, current_plan = stack.pop()
        if project_num == 0:
            distributions.append(current_plan)
            continue

        project_idx = project_num - 1
        target_profit = max_profits[project_num][remaining_lots]

        for cur_project_lots in range(remaining_lots + 1):
            prev_project_lots = remaining_lots - cur_project_lots
            prev_profit = max_profits[project_num - 1][prev_project_lots]
            cur_project_profit = _get_project_profit(
                profit_matrix, project_idx, cur_project_lots
            )
            if prev_profit + cur_project_profit == target_profit:
                next_plan = current_plan.copy()
                next_plan[project_idx] = cur_project_lots
                stack.append((project_num - 1, prev_project_lots, next_plan))

    return distributions


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
    _validate_table_types(profit_matrix)
    _validate_table_shape(profit_matrix)
    _validate_profit_values(profit_matrix)

    max_profits = _calculate_max_profits(profit_matrix)
    optimal_profit = max_profits[-1][-1]
    distributions = _restore_distributions(profit_matrix, max_profits)

    return Result(profit=optimal_profit, distributions=distributions)


def main():
    profit_matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
    print(get_invest_distributions(profit_matrix))


if __name__ == "__main__":
    main()
