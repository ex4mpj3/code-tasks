PATH_LENGTH_NOT_INT = "Длина маршрута не является целым числом"
PATH_LENGTH_NOT_POS = "Длина маршрута меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def count_a(n: int) -> int:
    if n == 1:
        return 0
    return count_b(n - 1) + count_c(n - 1)


def count_b(n: int) -> int:
    if n == 1:
        return 1
    return count_a(n - 1) + count_c(n - 1)


def count_c(n: int) -> int:
    if n == 1:
        return 1
    return count_a(n - 1) + count_b(n - 1)


def get_triangle_path_count(length: int) -> int:
    """Возвращает число замкнутых маршрутов заданной длины
    из вершины A в вершину A треугольника ABC.

    :param length: длина маршрута, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: число маршрутов
    """
    if type(length) is not int:
        raise TypeError(PATH_LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(PATH_LENGTH_NOT_POS)
    return count_a(length)


def check_binomial_args(n: int, k: int) -> None:
    if type(n) is not int:
        raise TypeError(NOT_INT_VALUE_TEMPL.format("n"))
    if type(k) is not int:
        raise TypeError(NOT_INT_VALUE_TEMPL.format("k"))
    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))
    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    check_binomial_args(n, k)
    res = 1
    for i in range(1, k + 1):
        res = res * (n - k + i) // i
    return res


def _binomial_rec(n: int, k: int) -> int:
    """Рекурсивный расчёт C(n, k) без проверки аргументов,
    аргументы проверяет binomial_coefficient_rec"""
    if k == 0:
        return 1
    return n * _binomial_rec(n - 1, k - 1) // k


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по соотношению C(n, k) = (n / k) * C(n - 1, k - 1).

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    check_binomial_args(n, k)
    return _binomial_rec(n, k)


def main():
    n = 4
    print(f"Количество маршрутов длиной {n} = {get_triangle_path_count(n)}")

    n = 30
    k = 20
    print(
        f"Биномиальный коэффициент (итеративно) при n, k ({n}, {k}) = ",
        binomial_coefficient_iter(n, k),
    )
    n = 5
    k = 2
    print(
        f"Биномиальный коэффициент (рекурсивно) при n, k ({n}, {k}) = ",
        binomial_coefficient_rec(n, k),
    )


if __name__ == "__main__":
    main()
