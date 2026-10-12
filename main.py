from collections import namedtuple

INF = float("inf")
TABLE_NOT_LISTS = "Таблица цен не является списком списков"
CELL_NOT_NUMBER = "Клетка таблицы не является числом или None"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])


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
    pass


def main():
    table = [[1.1, None], [3, 4]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
