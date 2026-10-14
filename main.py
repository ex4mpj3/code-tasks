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
    validate_strings(length)

    res = []

    f0(length, "", res)
    f1(length, "", res)

    return res


def f0(length, cur, res):
    new_cur = cur + "0"
    length -= 1

    if length == 0:
        res.append(new_cur)
        return

    f1(length, new_cur, res)


def f1(length, cur, res):
    new_cur = cur + "1"
    length -= 1

    if length == 0:
        res.append(new_cur)
        return

    f0(length, new_cur, res)
    f1(length, new_cur, res)


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    validate_binom(n, k)

    row = [1]
    for i in range(1, n + 1):
        new_row = [1]
        for j in range(1, min(i, k) + 1):
            if j == i:
                new_row.append(1)
            else:
                new_row.append(row[j - 1] + row[j])
        row = new_row

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
    validate_binom(n, k)

    # дополнитель используем мемоизацию, чтобы снизить рекурсии
    # количество вызовов и вычислений для больших значений n и k
    cache = {}

    return _pascal_rec(n, k, cache)


def _pascal_rec(n, k, cache):
    if k == 0 or k == n:
        return 1

    if (n, k) in cache:
        return cache[(n, k)]

    result = _pascal_rec(n - 1, k, cache) + _pascal_rec(n - 1, k - 1, cache)
    cache[(n, k)] = result

    return result


def validate_binom(n, k):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(NOT_INT_VALUE_TEMPL.format("n"))

    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError(NOT_INT_VALUE_TEMPL.format("k"))

    if n < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("n"))

    if k < 0:
        raise ValueError(NEGATIVE_VALUE_TEMPL.format("k"))

    if n < k:
        raise ValueError(N_LESS_THAN_K_ERROR_MSG)


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
