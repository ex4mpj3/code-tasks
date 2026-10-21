from collections import namedtuple

INF = float("inf")
TABLE_NOT_NUMBERS = "Таблица цен не является списком списков чисел"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])


def _validate_table(price_table):
    """Проверяет правильность таблицы цен."""
    if not isinstance(price_table, list):
        raise TypeError(TABLE_NOT_NUMBERS)

    if not price_table:
        raise ValueError(TABLE_NOT_RECT)

    if any(not isinstance(row, list) for row in price_table):
        raise TypeError(TABLE_NOT_NUMBERS)

    width = len(price_table[0])

    if width == 0 or any(len(row) != width for row in price_table):
        raise ValueError(TABLE_NOT_RECT)

    for row in price_table:
        for price in row:
            if isinstance(price, bool) or not isinstance(price, (int, float)):
                raise TypeError(TABLE_NOT_NUMBERS)


def get_min_cost_path(price_table: list[list[float | int]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз

    :param price_table: прямоугольная таблица цен посещения ячеек
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и списком индексов (строка, столбец)
    """
    _validate_table(price_table)
    height = len(price_table)
    width = len(price_table[0])
    min_costs = [[INF] * (width + 1) for _ in range(height + 1)]
    min_costs[1][1] = price_table[0][0]

    for row in range(1, height + 1):
        for col in range(1, width + 1):
            if row == 1 and col == 1:
                continue

            min_costs[row][col] = price_table[row - 1][col - 1] + min(
                min_costs[row - 1][col],
                min_costs[row][col - 1],
            )

    path = []
    row = height
    col = width
    while row > 1 or col > 1:
        path.append((row - 1, col - 1))
        if row == 1:
            col -= 1
        elif col == 1:
            row -= 1
        elif min_costs[row - 1][col] <= min_costs[row][col - 1]:
            row -= 1
        else:
            col -= 1
    path.append((0, 0))
    path.reverse()

    return Result(min_costs[height][width], path)


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
