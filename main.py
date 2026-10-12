LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: список строк
    """
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)
    if length == 1:
        return ["0", "1"]

    # После начального нуля суффикс обязан начинаться с единицы.
    return [
        "0" + suffix for suffix in _strings_starting_with_one(length - 1)
    ] + _strings_starting_with_one(length)


def _strings_starting_with_one(length: int) -> list[str]:
    """Возвращает допустимые строки длины length с начальной единицей."""
    if length == 1:
        return ["1"]
    return ["1" + suffix for suffix in generate_strings(length - 1)]


def _validate_binomial_arguments(n: int, k: int) -> None:
    """Проверяет одинаковые ограничения для обеих реализаций."""
    for name, value in (("n", n), ("k", k)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(NOT_INT_VALUE_TEMPL.format(name))
        if value < 0:
            raise ValueError(NEGATIVE_VALUE_TEMPL.format(name))
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
    _validate_binomial_arguments(n, k)
    if k == 0 or k == n:
        return 1

    # Начальная строка: C_0^0 = 1; в остальных столбцах сочетаний пока нет.
    coefficients = [1] + [0] * k
    for row in range(1, n + 1):
        # Идём справа налево, чтобы оба слагаемых были из предыдущей строки.
        for column in range(min(row, k), 0, -1):
            coefficients[column] += coefficients[column - 1]
    return coefficients[k]


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_binomial_arguments(n, k)
    if k == 0 or k == n:
        return 1
    return binomial_coefficient_rec(n - 1, k) + binomial_coefficient_rec(n - 1, k - 1)


def main():
    n = 2
    print(f"Строки длиной {n}:\n{generate_strings(n)}")

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
