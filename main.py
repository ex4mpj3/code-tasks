from collections import namedtuple
from typing import Any

INF = float("inf")
TABLE_NOT_NUMBERS = "Таблица цен не является списком списков чисел"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])


def _validate_table(price_table: Any) -> None:
    """Проверяет корректность таблицы цен, при ошибке вызывает исключение."""
    if type(price_table) is not list:
        raise TypeError(TABLE_NOT_NUMBERS)

    for row in price_table:
        if type(row) is not list:
            raise TypeError(TABLE_NOT_NUMBERS)
        for value in row:
            if type(value) not in (int, float):
                raise TypeError(TABLE_NOT_NUMBERS)

    if not price_table or not price_table[0]:
        raise ValueError(TABLE_NOT_RECT)

    row_len = len(price_table[0])
    if any(len(row) != row_len for row in price_table):
        raise ValueError(TABLE_NOT_RECT)


def _build_cost_table(price_table: list[list[float | int]]) -> list[list[float | int]]:
    """Строит таблицу минимальной стоимости до каждой ячейки с барьерной границей."""
    rows = len(price_table)
    columns = len(price_table[0])

    cost = [[INF] * (columns + 1) for _ in range(rows + 1)]
    cost[0][1] = 0

    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            cost[i][j] = price_table[i - 1][j - 1] + min(cost[i - 1][j], cost[i][j - 1])

    return cost


def _backtrack_path(cost: list[list[float | int]]) -> list[tuple[int, int]]:
    """Восстанавливает оптимальный путь от правого нижнего угла до (0, 0)."""
    i = len(cost) - 1
    j = len(cost[0]) - 1
    path = [(i - 1, j - 1)]

    while i > 1 or j > 1:
        if cost[i - 1][j] < cost[i][j - 1]:
            i -= 1
        else:
            j -= 1
        path.append((i - 1, j - 1))

    path.reverse()
    return path


def get_min_cost_path(price_table: list[list[float | int]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз.

    :param price_table: Прямоугольная таблица цен посещения ячеек
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и списком индексов (строка, столбец)
    """
    _validate_table(price_table)
    cost = _build_cost_table(price_table)
    path = _backtrack_path(cost)
    return Result(cost=cost[-1][-1], path=path)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
