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
    if type(length) is not int:
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)

    result_strings = []

    def add_zero(current_string):
        new_string = current_string + "0"
        if len(new_string) == length:
            result_strings.append(new_string)
        else:
            add_one(new_string)

    def add_one(current_string):
        new_string = current_string + "1"
        if len(new_string) == length:
            result_strings.append(new_string)
        else:
            add_zero(new_string)
            add_one(new_string)

    add_zero("")
    add_one("")
    return result_strings


def _validate_binomial(n, k):
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
    _validate_binomial(n, k)

    coefficients = [0] * (k + 1)
    coefficients[0] = 1

    for current_n in range(1, n + 1):
        for current_k in range(min(current_n, k), 0, -1):
            coefficients[current_k] += coefficients[current_k - 1]

    return coefficients[k]


def _binomial_rec(n: int, k: int) -> int:
    if k == 0 or k == n:
        return 1
    return _binomial_rec(n - 1, k) + _binomial_rec(n - 1, k - 1)


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_binomial(n, k)
    return _binomial_rec(n, k)


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
