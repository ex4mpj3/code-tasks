LENGTH_NOT_INT = "Длина строки не является целым числом"
LENGTH_NOT_POS = "Длина строки меньше единицы"
NOT_INT_VALUE_TEMPL = "Параметр {0} не является целым числом"
NEGATIVE_VALUE_TEMPL = "Параметр {0} отрицательный"
N_LESS_THAN_K_ERROR_MSG = "Параметр n меньше чем k"


def _validate_binomial_input(n: int, k: int):
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


def _generate_strings_ending_with_zero(length: int) -> list[str]:
    if length == 1:
        return ["0"]
    
    prev_strings = _generate_strings_ending_with_one(length - 1)
    return [s + "0" for s in prev_strings]


def _generate_strings_ending_with_one(length: int) -> list[str]:
    if length == 1:
        return ["1"]
    
    from_zero = _generate_strings_ending_with_zero(length - 1)
    from_one = _generate_strings_ending_with_one(length - 1)
    
    combined = from_zero + from_one
    return [s + "1" for s in combined]


def generate_strings(length: int) -> list[str]:
    """Возвращает строки заданной длины, состоящие из 0 и 1, где никакие
    два нуля не стоят рядом.

    :param length: длина строки, целое число не меньше 1
    :raise TypeError: если length не целое
    :raise ValueError: если length меньше единицы
    :return: список строк
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError(LENGTH_NOT_INT)
    if length < 1:
        raise ValueError(LENGTH_NOT_POS)
    
    if length == 0:
        return [""]

    ending_with_zero = _generate_strings_ending_with_zero(length)
    ending_with_one = _generate_strings_ending_with_one(length)
    
    return ending_with_zero + ending_with_one


def binomial_coefficient_iter(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k итеративно.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_binomial_input(n, k)
    
    if k == 0 or k == n:
        return 1
    
    # Оптимизация: C(n, k) = C(n, n-k)
    if k > n // 2:
        k = n - k

    dp = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = 1
    
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i][j] = dp[i-1][j] + dp[i-1][j-1]
            
    return dp[n][k]


def binomial_coefficient_rec(n: int, k: int) -> int:
    """Вычисляет биномиальный коэффициент из n по k рекурсивно
    по правилу Паскаля.

    :param n: число элементов множества
    :param k: число выбираемых элементов
    :raise TypeError: если n или k не целое
    :raise ValueError: если n или k отрицательные либо n меньше k
    :return: значение биномиального коэффициента
    """
    _validate_binomial_input(n, k)
    
    if k == 0 or k == n:
        return 1
    
    # Оптимизация: C(n, k) = C(n, n-k)
    if k > n // 2:
        k = n - k

    return binomial_coefficient_rec(n - 1, k) + binomial_coefficient_rec(n - 1, k - 1)


def main():
    n_str = 4
    print(f"Строки длиной {n_str}:\n{generate_strings(n_str)}")

    n_iter = 30
    k_iter = 20
    print(
        f"Биномиальный коэффициент (итеративно) при n, k ({n_iter}, {k_iter}) = ",
        binomial_coefficient_iter(n_iter, k_iter),
    )
    n_rec = 5
    k_rec = 2
    print(
        f"Биномиальный коэффициент (рекурсивно) при n, k ({n_rec}, {k_rec}) = ",
        binomial_coefficient_rec(n_rec, k_rec),
    )


if __name__ == "__main__":
    main()