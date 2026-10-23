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


def get_invest_distribution(profit_matrix: list[list[float | int]]) -> Result:
    """Возвращает максимальную прибыль и распределение всех лотов по проектам.
    План восстанавливается после расчёта прибыли

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distribution
    """
    if not isinstance(profit_matrix, list):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
        
    if not profit_matrix or not isinstance(profit_matrix[0], list) or not profit_matrix[0]:
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)

    n = len(profit_matrix)
    k = len(profit_matrix[0])

    for row in profit_matrix:
        if not isinstance(row, list) or len(row) != k:
            raise ValueError(ErrorMessages.TABLE_NOT_RECT)

    for i in range(n):
        for j in range(k):
            cell = profit_matrix[i][j]
            if isinstance(cell, bool) or not isinstance(cell, (int, float)):
                raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)

    for i in range(n):
        for j in range(k):
            if profit_matrix[i][j] < 0:
                raise ProfitValueError(
                    ErrorMessages.NEG_PROFIT, project_idx=i, row_idx=j
                )
            if j > 0 and profit_matrix[i][j] < profit_matrix[i][j - 1]:
                raise ProfitValueError(
                    ErrorMessages.DECR_PROFIT, project_idx=i, row_idx=j
                )

    F = [[UNREACHABLE] * (k + 1) for _ in range(n + 1)]
    F[0][0] = 0

    for i in range(1, n + 1):
        for j in range(k + 1):
            best = UNREACHABLE
            for x in range(j + 1):
                prev = F[i - 1][j - x]
                if prev == UNREACHABLE:
                    continue
                p = 0 if x == 0 else profit_matrix[i - 1][x - 1]
                cand = prev + p
                if cand > best:
                    best = cand
            F[i][j] = best

    distribution = [0] * n
    j = k
    for i in range(n, 0, -1):
        for x in range(j + 1):
            prev = F[i - 1][j - x]
            if prev == UNREACHABLE:
                continue
            p = 0 if x == 0 else profit_matrix[i - 1][x - 1]
            if prev + p == F[i][j]:
                distribution[i - 1] = x
                j -= x
                break

    return Result(profit=F[n][k], distribution=distribution)


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