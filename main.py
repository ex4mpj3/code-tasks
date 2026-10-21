from collections import namedtuple
from enum import StrEnum
from math import isclose

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


def _check_types(profit_matrix) -> None:
    """Проверяет, что таблица — список списков чисел (bool числом не считается)"""
    if not isinstance(profit_matrix, list):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    for row in profit_matrix:
        if not isinstance(row, list):
            raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
        for value in row:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)


def _check_shape(profit_matrix: list[list[float | int]]) -> None:
    """Проверяет, что таблица непустая и прямоугольная"""
    if not profit_matrix or not profit_matrix[0]:
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)
    width = len(profit_matrix[0])
    for row in profit_matrix:
        if len(row) != width:
            raise ValueError(ErrorMessages.TABLE_NOT_RECT)


def _check_profit_values(profit_matrix: list[list[float | int]]) -> None:
    """Проверяет неотрицательность и неубывание прибыли по каждому столбцу"""
    for row_idx, row in enumerate(profit_matrix):
        for project_idx, value in enumerate(row):
            if value < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, project_idx, row_idx)
    for row_idx in range(1, len(profit_matrix)):
        for project_idx, value in enumerate(profit_matrix[row_idx]):
            if value < profit_matrix[row_idx - 1][project_idx]:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, project_idx, row_idx)


def _project_profit(profit_matrix: list[list[float | int]], project, lots):
    """P_i(x): прибыль проекта при вложении lots лотов, P_i(0) = 0"""
    if lots == 0:
        return 0
    return profit_matrix[lots - 1][project]


def _fill_table(profit_matrix: list[list[float | int]]) -> list[list[float]]:
    """Прямой ход: таблица F(i, j), хранятся только значения прибыли"""
    lots_count = len(profit_matrix)
    projects_count = len(profit_matrix[0])
    table = [[UNREACHABLE] * (lots_count + 1) for _ in range(projects_count + 1)]
    table[0][0] = 0
    for i in range(1, projects_count + 1):
        for j in range(lots_count + 1):
            table[i][j] = max(
                table[i - 1][j - x] + _project_profit(profit_matrix, i - 1, x)
                for x in range(j + 1)
            )
    return table


def _restore_distribution(
    profit_matrix: list[list[float | int]], table: list[list[float]]
) -> list[int]:
    """Обратный ход по готовой таблице F, начиная с F(n, k)"""
    projects_count = len(table) - 1
    lots_left = len(table[0]) - 1
    distribution = [0] * projects_count
    for i in range(projects_count, 0, -1):
        for x in range(lots_left + 1):
            candidate = table[i - 1][lots_left - x] + _project_profit(
                profit_matrix, i - 1, x
            )
            if isclose(candidate, table[i][lots_left]):
                distribution[i - 1] = x
                lots_left -= x
                break
    return distribution


def get_invest_distribution(profit_matrix: list[list[float | int]]) -> Result:
    """Возвращает максимальную прибыль и распределение всех лотов по проектам.
    План восстанавливается после расчёта прибыли

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distribution
    """
    _check_types(profit_matrix)
    _check_shape(profit_matrix)
    _check_profit_values(profit_matrix)
    table = _fill_table(profit_matrix)
    distribution = _restore_distribution(profit_matrix, table)
    return Result(table[-1][-1], distribution)


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
