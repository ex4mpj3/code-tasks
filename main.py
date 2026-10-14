NOT_LIST = "Набор не является списком"
NOT_COMPARABLE = "Элементы набора несравнимы"


def recursive_sort(items: list) -> list:
    """Возвращает новый список, упорядоченный по неубыванию.

    Алгоритм: сортировка слиянием.
    Элементы должны быть попарно сравнимы операцией <.

    :param items: список сравнимых элементов
    :raise TypeError: если items не список либо элементы несравнимы
    :return: новый отсортированный список
    """
    if not isinstance(items, list):
        raise TypeError(NOT_LIST)

    try:
        return merge_sort(items)
    except TypeError as error:
        raise TypeError(NOT_COMPARABLE) from error


def merge_sort(items: list) -> list:
    """Рекурсивно сортирует список слиянием.

    Делит список пополам, сортирует половины и сливает их.

    :param items: список сравнимых элементов
    :return: новый отсортированный список
    """
    if len(items) <= 1:
        return items.copy()

    middle = len(items) // 2
    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])
    return merge(left, right)


def merge(left: list, right: list) -> list:
    """Сливает два отсортированных списка в один отсортированный.

    При равенстве первым берётся элемент из left,
    поэтому порядок равных элементов сохраняется.

    :param left: отсортированный список
    :param right: отсортированный список
    :return: новый отсортированный список из элементов обоих
    """
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if right[j] < left[i]:
            result.append(right[j])
            j += 1
        else:
            result.append(left[i])
            i += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def main():
    items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
    print("Пример рекурсивной сортировки")
    print(f"Исходный список: {items}")
    print(f"Отсортированный список: {recursive_sort(items)}")


if __name__ == "__main__":
    main()
