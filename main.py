from functools import lru_cache


def get_tridiagonal_determinant(matrix: list[list[int]]) -> int:
    """Рекурсивное вычисление определителя трёхдиагональной матрицы разложением.

    :param matrix: квадратная целочисленная трёхдиагональная матрица
        порядка не меньше 1 с постоянными значениями на каждой
        из трёх диагоналей
    :raises Exception: если matrix не является такой матрицей
    :return: значение определителя
    """
    _validate(matrix)

    n = len(matrix)
    a = matrix[0][0]
    b = matrix[0][1] if n > 1 else 0
    c = matrix[1][0] if n > 1 else 0

    return _tridiagonal_determinant(a, b, c, n)


def _validate(matrix: list[list[int]]) -> None:
    """Проверяет, что matrix — трёхдиагональная матрица с постоянными
    значениями на диагоналях."""
    _validate_shape(matrix)
    _validate_integers(matrix)
    _validate_diagonals(matrix)


def _validate_shape(matrix: list[list[int]]) -> None:
    if not isinstance(matrix, list):
        raise Exception("Матрица должна быть списком строк.")
    if len(matrix) == 0:
        raise Exception("Матрица не должна быть пустой.")

    n = len(matrix)
    for row in matrix:
        if not isinstance(row, list):
            raise Exception("Каждая строка матрицы должна быть списком.")
        if len(row) != n:
            raise Exception("Матрица должна быть квадратной: все строки одной длины.")


def _validate_integers(matrix: list[list[int]]) -> None:
    """Проверяет, что все элементы matrix — целые числа (не bool)."""
    for row in matrix:
        for value in row:
            if not isinstance(value, int) or isinstance(value, bool):
                raise Exception("Все элементы матрицы должны быть целыми числами.")


def _validate_diagonals(matrix: list[list[int]]) -> None:
    n = len(matrix)
    a = matrix[0][0]
    b = matrix[0][1] if n > 1 else None
    c = matrix[1][0] if n > 1 else None

    for i in range(n):
        for j in range(n):
            expected = _expected_value(i, j, a, b, c)
            if matrix[i][j] != expected:
                raise Exception(
                    "Матрица должна быть трёхдиагональной с постоянными "
                    "значениями на каждой из трёх диагоналей."
                )


def _expected_value(i: int, j: int, a: int, b: int | None, c: int | None) -> int:
    if i == j:
        return a
    if j == i + 1:
        return b
    if i == j + 1:
        return c
    return 0


@lru_cache(maxsize=None)
def _tridiagonal_determinant(a: int, b: int, c: int, n: int) -> int:
    """Рекурсивно вычисляет определитель трёхдиагональной матрицы порядка n
    по рекуррентному соотношению x_n = a * x_{n-1} - b * c * x_{n-2}.

    :param a: значение на главной диагонали
    :param b: значение на наддиагонали
    :param c: значение на поддиагонали
    :param n: порядок матрицы, целое число не меньше 1
    :return: значение определителя
    """
    if n == 1:
        return a
    if n == 2:
        return a * a - b * c
    return a * _tridiagonal_determinant(
        a, b, c, n - 1
    ) - b * c * _tridiagonal_determinant(a, b, c, n - 2)


def main():
    matrix = [[2, -3, 0, 0], [5, 2, -3, 0], [0, 5, 2, -3], [0, 0, 5, 2]]
    print("Трехдиагональная матрица")
    for row in matrix:
        print(row)

    print(f"Определитель матрицы равен {get_tridiagonal_determinant(matrix)}")


if __name__ == "__main__":
    main()
