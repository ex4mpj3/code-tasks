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
    validate_length(length)
    strings = []
    extend_with_zero("", length, strings)
    extend_with_one("", length, strings)
    return strings


def extend_with_zero(prefix: str, length: int, strings: list[str]) -> None:
    string = prefix + "0"
    if len(string) == length:
        strings.append(string)
    else:
        extend_with_one(string, length, strings)


def extend_with_one(prefix: str, length: int, strings: list[str]) -> None:
    string = prefix + "1"
    if len(string) == length:
        strings.append(string)
    else:
        extend_with_zero(string, length, strings)
        extend_with_one(string, length, strings)


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    validate_binomial_parameters(n, k)
    row = [1]
    for _ in range(n):
        inner = [row[j - 1] + row[j] for j in range(1, len(row))]
        row = ([1] + inner + [1])[: k + 1]
    return row[k]


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    validate_binomial_parameters(n, k)
    return calculate_binomial(n, k)


def calculate_binomial(n: int, k: int) -> int:
    if k == 0 or k == n:
        return 1
    return calculate_binomial(n - 1, k) + calculate_binomial(n - 1, k - 1)


def validate_length(length: int) -> None:
    if not is_integer(length):
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)


def validate_binomial_parameters(n: int, k: int) -> None:
    validate_non_negative_integer("n", n)
    validate_non_negative_integer("k", k)
    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


def validate_non_negative_integer(name: str, value: int) -> None:
    if not is_integer(value):
        raise TypeError(NOT_INT_VALUE_TEMPL.format(name))
    if value < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format(name))


def is_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


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
