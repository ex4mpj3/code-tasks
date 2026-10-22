def generate_permutations_rec(elements: list) -> list[list]:
    """Возвращает все перестановки элементов списка.

    Порядок перестановок в списке не фиксируется. Повторы и пропуски
    недопустимы.

    :param elements: список любых элементов
    :raises TypeError: аргумент не является списком
    :return: список перестановок; для пустого списка — список из одной
        пустой перестановки
    """
    pass


def generate_permutations_iter(elements: list) -> list[list]:
    """Возвращает все перестановки элементов списка.

    Итеративная реализация, без рекурсии. Порядок перестановок
    в списке не фиксируется. Повторы и пропуски недопустимы.

    :param elements: список любых элементов
    :raises TypeError: аргумент не является списком
    :return: список перестановок; для пустого списка — список из одной
        пустой перестановки
    """
    pass


def main():
    for elements in ([], ["a"], ["a", "b", "c"]):
        print(f"{elements}, рекурсивно: {generate_permutations_rec(elements)}")
        print(f"{elements}, итеративно: {generate_permutations_iter(elements)}")


if __name__ == "__main__":
    main()
