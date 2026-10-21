from collections import namedtuple

INF = float("inf")
TABLE_NOT_LISTS = "Таблица цен не является списком списков"
CELL_NOT_NUMBER = "Клетка таблицы не является числом или None"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])

def _validate_data(price_table: list[list[float | int | None]]):
    if not isinstance(price_table, list) or any(
        not isinstance(row, list) for row in price_table
    ):
        raise TypeError(TABLE_NOT_LISTS)

    if not price_table or not price_table[0]:
        raise ValueError(TABLE_NOT_RECT)

    col_count = len(price_table[0])

    for row in price_table:
        if len(row) != col_count:
            raise ValueError(TABLE_NOT_RECT)

        for value in row:
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, (int, float))
            ):
                raise TypeError(CELL_NOT_NUMBER)

def get_min_cost_path(price_table: list[list[float | int | None]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз. None в клетке
    запрещает посещение. Если пути нет, cost и path равны None

    :param price_table: прямоугольная таблица цен, None — запрещённая клетка
    :raise TypeError: если аргумент не список списков либо клетка не число
        и не None
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и путём либо Result(None, None)
    """

    _validate_data(price_table)
    
    height = len(price_table)
    width = len(price_table[0])

    min_costs = []
    for _ in range(height + 1):
        min_costs.append([INF for _ in range(width + 1)])

    min_costs[0][1] = 0

    for row in range(height):
        for col in range(width):
            price = price_table[row][col]
            if price is None:
                continue

            min_costs[row + 1][col + 1] = price + min(
                min_costs[row][col + 1],
                min_costs[row + 1][col],
            )

    total_cost = min_costs[height][width]
    if total_cost == INF:
        return Result(None, None)

    path = []
    row = height - 1
    col = width - 1

    while True:
        path.append((row, col))

        if row == 0 and col == 0:
            break
        if row == 0:
            col -= 1
        elif col == 0:
            row -= 1
        elif min_costs[row][col + 1] <= min_costs[row + 1][col]:
            row -= 1
        else:
            col -= 1

    path.reverse()
    return Result(total_cost, path)


def main():
    table = [[1.1, None], [3, 4]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
