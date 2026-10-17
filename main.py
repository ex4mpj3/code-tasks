from collections import namedtuple

INF = float("inf")
TABLE_NOT_NUMBERS = "Таблица цен не является списком списков чисел"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])


def validate_table(price_table: list) -> None:
    """Проверяем таблицу цен, при ошибке вызываем исключение"""
    # таблица должна быть списком списков чисел
    if not isinstance(price_table, list):
        raise TypeError(TABLE_NOT_NUMBERS)
    for row in price_table:
        if not isinstance(row, list):
            raise TypeError(TABLE_NOT_NUMBERS)
        for value in row:
            if type(value) not in (int, float):
                raise TypeError(TABLE_NOT_NUMBERS)

    # таблица не пустая и все строки одинаковой длины
    if len(price_table) == 0 or len(price_table[0]) == 0:
        raise ValueError(TABLE_NOT_RECT)
    for row in price_table:
        if len(row) != len(price_table[0]):
            raise ValueError(TABLE_NOT_RECT)


def build_cost_table(price_table: list) -> list:
    """Строим таблицу минимальной стоимости до каждой ячейки"""
    rows = len(price_table)
    columns = len(price_table[0])
    # cost [i][j] = минимальная стоимость пути из (0, 0) в (i, j)
    cost = [[0] * columns for _ in range(rows)]
    for i in range(rows):
        for j in range(columns):
            if i == 0 and j == 0:
                cost[i][j] = price_table[i][j]
            elif i == 0:
                cost[i][j] = cost[i][j - 1] + price_table[i][j]
            elif j == 0:
                cost[i][j] = cost[i - 1][j] + price_table[i][j]
            else:
                cheapest = min(cost[i - 1][j], cost[i][j - 1])
                cost[i][j] = cheapest + price_table[i][j]
    return cost


def backtrack_path(cost: list) -> list:
    """Обратный путь от 2,2 до 0,0 по таблице"""
    i = len(cost) - 1
    j = len(cost[0]) - 1
    path = [(i, j)]
    # Идем обратно по таблице выбирая мин. стоимость.
    while i > 0 or j > 0:
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            if cost[i - 1][j] < cost[i][j - 1]:
                i -= 1
            else:
                j -= 1
        path.append((i, j))
    path.reverse()
    return path


def get_min_cost_path(price_table: list[list[float | int]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз

    :param price_table: прямоугольная таблица цен посещения ячеек
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и списком индексов (строка, столбец)
    """
    validate_table(price_table)
    cost = build_cost_table(price_table)
    path = backtrack_path(cost)
    return Result(cost=cost[-1][-1], path=path)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print("Таблица цен:", table)
    print("Таблица минимальных стоимостей:", build_cost_table(table))
    print("Результат:", get_min_cost_path(table))


if __name__ == "__main__":
    main()
