from functools import cache
from typing import Any

LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def validate(n: Any, k: Any) -> None:
    """Проводит валидацию для функций, работающих с биноминальным коэффициентом, вызывает ошибку при некорректных входящих данных"""
    for name, val in (("n", n), ("k", k)):
        if type(val) is not int:
            raise TypeError(NOT_INT_VALUE_TEMPL.format(name))
        if val < 0:
            raise ValueError(NEGATIVE_VALUE_TEMPL.format(name))

    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


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

    def starts_with_0(n: int) -> list[str]:
        """Генерирует строки длины n, начинающиеся с '0'"""
        if n == 1:
            return ["0"]
        return ["0" + s for s in starts_with_1(n - 1)]

    def starts_with_1(n: int) -> list[str]:
        """Генерирует строки длины n, начинающиеся с '1'"""
        if n == 1:
            return ["1"]
        tails = starts_with_0(n - 1) + starts_with_1(n - 1)
        return ["1" + s for s in tails]

    return starts_with_0(length) + starts_with_1(length)


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    validate(n, k)
    if k in (0, n):
        return 1
    # Оптимизация на основе свойства зеркальности биноминальных коэффициентов
    if k > n - k:
        k = n - k
    result = 1
    for i in range(k):
        result = (result * (n - i)) // (i + 1)
    return result


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    validate(n, k)

    @cache
    def inner_recursion(n: int, k: int) -> int:
        if k in (0, n):
            return 1
        return inner_recursion(n - 1, k - 1) + inner_recursion(n - 1, k)

    return inner_recursion(n, k)


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
