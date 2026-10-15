from collections import namedtuple
from enum import StrEnum

UNREACHABLE = float("-inf")


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках"""

    TABLE_NOT_NUMBERS = "Таблица прибыли не является списком списков чисел"
    TABLE_NOT_RECT = "Таблица прибыли не является прямоугольной матрицей"
    NEG_PROFIT = "Значение прибыли не может быть отрицательно"
    DECR_PROFIT = "Значение прибыли не может убывать с ростом инвестиций"


Result = namedtuple("Result", ["profit", "distribution"])


class ProfitValueError(Exception):
    def __init__(self, message: str, project_idx: int, row_idx: int) -> None:
        self.project_idx = project_idx
        self.row_idx = row_idx
        super().__init__(message)


def _validate_profit_matrix(profit_matrix: list[list[float | int]]) -> None:
    """Проверяет форму, типы и неубывание прибыли для каждого проекта."""
    if not isinstance(profit_matrix, list) or any(
        not isinstance(row, list) for row in profit_matrix
    ):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    if (
        not profit_matrix
        or not profit_matrix[0]
        or any(len(row) != len(profit_matrix[0]) for row in profit_matrix)
    ):
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)

    for row_idx, row in enumerate(profit_matrix):
        for project_idx, profit in enumerate(row):
            if isinstance(profit, bool) or not isinstance(profit, (int, float)):
                raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
            if profit < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, project_idx, row_idx)
            if row_idx > 0 and profit < profit_matrix[row_idx - 1][project_idx]:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, project_idx, row_idx)


def get_invest_distribution(profit_matrix: list[list[float | int]]) -> Result:
    """Возвращает максимальную прибыль и распределение всех лотов по проектам

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distribution
    """
    _validate_profit_matrix(profit_matrix)
    levels = len(profit_matrix)
    projects = len(profit_matrix[0])
    # Без проектов достижимо только распределение нуля лотов.
    previous_profit = [0] + [UNREACHABLE] * levels
    chosen_lots = [[0] * (levels + 1) for _ in range(projects)]

    for project_idx in range(projects):
        current_profit = [UNREACHABLE] * (levels + 1)
        for total_lots in range(levels + 1):
            for project_lots in range(total_lots + 1):
                prefix_profit = previous_profit[total_lots - project_lots]
                if prefix_profit == UNREACHABLE:
                    continue
                project_profit = (
                    profit_matrix[project_lots - 1][project_idx] if project_lots else 0
                )
                candidate = prefix_profit + project_profit
                if candidate > current_profit[total_lots]:
                    current_profit[total_lots] = candidate
                    chosen_lots[project_idx][total_lots] = project_lots
        previous_profit = current_profit

    distribution = [0] * projects
    remaining_lots = levels
    for project_idx in range(projects - 1, -1, -1):
        project_lots = chosen_lots[project_idx][remaining_lots]
        distribution[project_idx] = project_lots
        remaining_lots -= project_lots
    return Result(previous_profit[levels], distribution)


def main():
    profit_matrix = [
        [15, 18, 16, 17],
        [20, 22, 23, 19],
        [26, 28, 27, 25],
        [34, 33, 29, 31],
        [40, 39, 41, 37],
    ]
    print(get_invest_distribution(profit_matrix))


if __name__ == "__main__":
    main()
