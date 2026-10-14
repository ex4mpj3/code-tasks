PATH_LENGTH_NOT_INT = "Длина маршрута не является целым числом"
PATH_LENGTH_NOT_POS = "Длина маршрута меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def _routes_end_a(n: int) -> int:
    """Число маршрутов длины n, которые начинаются и заканчиваются в A.

    a(1) = 0, a(n) = b(n - 1) + c(n - 1).
    """
    if n == 1:
        return 0
    return _routes_end_b(n - 1) + _routes_end_c(n - 1)


def _routes_end_b(n: int) -> int:
    """Число маршрутов длины n, которые начинаются в A и заканчиваются в B.

    b(1) = 1, b(n) = a(n - 1) + c(n - 1).
    """
    if n == 1:
        return 1
    return _routes_end_a(n - 1) + _routes_end_c(n - 1)


def _routes_end_c(n: int) -> int:
    """Число маршрутов длины n, которые начинаются в A и заканчиваются в C.

    c(1) = 1, c(n) = a(n - 1) + b(n - 1).
    """
    if n == 1:
        return 1
    return _routes_end_a(n - 1) + _routes_end_b(n - 1)


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
    return _routes_end_a(length)


def _check_int_param(value: int, name: str) -> None:
    """Проверяет, что параметр - целое неотрицательное число.

    :param value: значение параметра
    :param name: имя параметра для текста ошибки
    :raise TypeError: если value не целое
    :raise ValueError: если value отрицательное
    """
    if type(value) is not int:
        raise TypeError(NOT_INT_VALUE_TEMPL.format(name))
    if value < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format(name))


def _check_binomial_args(n: int, k: int) -> None:
    """Общая проверка входа для обеих функций биномиального коэффициента.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    """
    _check_int_param(n, "n")
    _check_int_param(k, "k")
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
    _check_binomial_args(n, k)
    # Начинаем с C(n - k, 0) = 1 и k раз применяем
    # C(m, j) = m / j * C(m - 1, j - 1), поднимаясь до C(n, k).
    value = 1
    m = n - k
    for j in range(1, k + 1):
        m += 1
        value = value * m // j
    return value


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по соотношению C(n, k) = (n / k) * C(n - 1, k - 1).

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _check_binomial_args(n, k)

    def step(m: int, j: int) -> int:
        if j == 0:
            return 1
        return m * step(m - 1, j - 1) // j

    return step(n, k)


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
