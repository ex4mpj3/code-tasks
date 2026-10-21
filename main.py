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
    """Выполняет валидацию таблицы прибыли.

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    """
    if not isinstance(profit_matrix, list):
        raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
    if (
        not profit_matrix
        or not isinstance(profit_matrix[0], list)
        or not profit_matrix[0]
    ):
        raise ValueError(ErrorMessages.TABLE_NOT_RECT)

    num_projects = len(profit_matrix[0])

    for r_idx, row in enumerate(profit_matrix):
        if not isinstance(row, list) or len(row) != num_projects:
            raise ValueError(ErrorMessages.TABLE_NOT_RECT)
        for c_idx, profit_val in enumerate(row):
            if not isinstance(profit_val, (int, float)) or isinstance(profit_val, bool):
                raise TypeError(ErrorMessages.TABLE_NOT_NUMBERS)
            if profit_val < 0:
                raise ProfitValueError(ErrorMessages.NEG_PROFIT, c_idx, r_idx)

            if r_idx > 0 and profit_val < profit_matrix[r_idx - 1][c_idx]:
                raise ProfitValueError(ErrorMessages.DECR_PROFIT, c_idx, r_idx)


def get_invest_distribution(profit_matrix: list[list[float | int]]) -> Result:
    """Возвращает максимальную прибыль и распределение всех лотов по проектам

    :param profit_matrix: строки — уровни вложения, столбцы — проекты
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :raise ProfitValueError: если прибыль отрицательная или убывает по столбцу
    :return: Result с полями profit и distribution
    """
    _validate_profit_matrix(profit_matrix)

    num_levels = len(profit_matrix)
    num_projects = len(profit_matrix[0])

    F = [[0.0] * (num_levels + 1) for _ in range(num_projects + 1)]

    P = [[0] * (num_levels + 1) for _ in range(num_projects + 1)]

    for i in range(1, num_projects + 1):
        for j in range(num_levels + 1):
            max_profit_for_ij = UNREACHABLE
            best_lots_for_project_i = 0

            for x in range(j + 1):
                profit_current_project = 0
                if x > 0:
                    profit_current_project = profit_matrix[x - 1][i - 1]

                current_total_profit = F[i - 1][j - x] + profit_current_project

                if current_total_profit > max_profit_for_ij:
                    max_profit_for_ij = current_total_profit
                    best_lots_for_project_i = x

            F[i][j] = max_profit_for_ij
            P[i][j] = best_lots_for_project_i

    distribution = [0] * num_projects
    current_lots = num_levels
    for i in range(num_projects, 0, -1):
        lots_for_current_project = P[i][current_lots]
        distribution[i - 1] = lots_for_current_project
        current_lots -= lots_for_current_project

    return Result(profit=F[num_projects][num_levels], distribution=distribution)


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
