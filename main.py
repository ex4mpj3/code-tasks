from collections import namedtuple

INF = float("inf")
TABLE_NOT_NUMBERS = "Таблица цен не является списком списков чисел"
TABLE_NOT_RECT = "Таблица цен не является прямоугольной матрицей"

Result = namedtuple("Result", ["cost", "path"])


def get_min_cost_path(price_table: list[list[float | int]]) -> Result:
    """Возвращает путь минимальной стоимости из левого верхнего угла
    таблицы в правый нижний. Ходы только вправо или вниз

    :param price_table: прямоугольная таблица цен посещения ячеек
    :raise TypeError: если аргумент не список списков чисел
    :raise ValueError: если таблица пустая или непрямоугольная
    :return: Result со стоимостью и списком индексов (строка, столбец)
    """
    pass


def main():
    table = [[1, 2, 2], [3, 4, 2], [1, 1, 2]]
    print(get_min_cost_path(table))


if __name__ == "__main__":
    main()
