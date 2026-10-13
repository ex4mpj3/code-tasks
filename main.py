PATH_LENGTH_NOT_INT = "Длина маршрута не является целым числом"
PATH_LENGTH_NOT_POS = "Длина маршрута меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def _paths_to_a(len: int) -> int:
    """Число маршрутов длины length из A в A. Вход уже проверен."""
    if len == 0:
        return 1
    return _paths_to_b(len - 1) + _paths_to_c(len - 1)


def _paths_to_b(len: int) -> int:
    """Число маршрутов длины length из A в B. Вход уже проверен."""
    if len == 0:
        return 0
    return _paths_to_a(len - 1) + _paths_to_c(len - 1)


def _paths_to_c(len: int) -> int:
    """Число маршрутов длины length из A в C. Вход уже проверен."""
    if len == 0:
        return 0
    return _paths_to_a(len - 1) + _paths_to_b(len - 1)


def get_triangle_path_count(length: int) -> int:
    """Возвращает число замкнутых маршрутов заданной длины
    из вершины A в вершину A треугольника ABC.

    :param length: длина маршрута, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: число маршрутов
    """
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError(PATH_LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(PATH_LENGTH_NOT_POS)
    return _paths_to_a(length)


def _validate_binomial(n: int, k: int) -> None:
    """Проверяет параметры n и k одинаково для обеих функций.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    """
    for name, value in (("n", n), ("k", k)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(NOT_INT_VALUE_TEMPL.format(name))
        if value < 0:
            raise ValueError(NEGATIVE_VALUE_TEMPL.format(name))
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def _binomial_recursive(n: int, k: int) -> int:
    """Рекурсивное ядро C(n, k) = (n / k) * C(n - 1, k - 1). Вход проверен."""
    if k == 0:
        return 1
    return n * _binomial_recursive(n - 1, k - 1) // k


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_binomial(n, k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по соотношению C(n, k) = (n / k) * C(n - 1, k - 1).

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_binomial(n, k)
    return _binomial_recursive(n, k)


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
