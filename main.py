from collections import namedtuple

TABLE_NOT_LISTS = "Таблица цен не является списком списков"
CELL_NOT_NUMBER = "Клетка таблицы не является числом или None"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])


def _validate_price_table(price_table):
    if not isinstance(price_table, list) or any(
        not isinstance(row, list) for row in price_table
    ):
        raise TypeError(TABLE_NOT_LISTS)

    if not price_table or not price_table[0]:
        raise ValueError(TABLE_NOT_RECT)

    width = len(price_table[0])
    for row in price_table:
        if len(row) != width:
            raise ValueError(TABLE_NOT_RECT)
        for price in row:
            if price is not None and (
                isinstance(price, bool) or not isinstance(price, (int, float))
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
    _validate_price_table(price_table)
    height = len(price_table)
    width = len(price_table[0])

    min_cost = [[None] * width for _ in range(height)]
    previous = [[None] * width for _ in range(height)]
    min_cost[0][0] = price_table[0][0]

    for row in range(height):
        for column in range(width):
            price = price_table[row][column]
            if price is None or (row == 0 and column == 0):
                continue

            if row > 0 and min_cost[row - 1][column] is not None:
                min_cost[row][column] = min_cost[row - 1][column] + price
                previous[row][column] = (row - 1, column)

            if column > 0 and min_cost[row][column - 1] is not None:
                cost_from_left = min_cost[row][column - 1] + price
                if (
                    min_cost[row][column] is None
                    or cost_from_left < min_cost[row][column]
                ):
                    min_cost[row][column] = cost_from_left
                    previous[row][column] = (row, column - 1)

    if min_cost[-1][-1] is None:
        return Result(None, None)

    path = []
    position = (height - 1, width - 1)
    while position is not None:
        path.append(position)
        position = previous[position[0]][position[1]]
    path.reverse()

    return Result(min_cost[-1][-1], path)


def main():
    table = [[1.1, None], [3, 4]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
