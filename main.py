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
    pass


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
