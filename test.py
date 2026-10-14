import random
import unittest

from main import NOT_COMPARABLE, NOT_LIST, recursive_sort


class Card:
    """Карточка, которая сравнивается только операцией < по value"""

    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __lt__(self, other):
        return self.value < other.value


class TestRecursiveSort(unittest.TestCase):
    """Набор тестов рекурсивной сортировки"""

    def test_empty(self):
        """Пустой список"""
        self.assertEqual(recursive_sort([]), [])

    def test_one(self):
        """Один элемент"""
        self.assertEqual(recursive_sort([7]), [7])

    def test_two(self):
        """Два элемента"""
        self.assertEqual(recursive_sort([2, 1]), [1, 2])

    def test_odd_length(self):
        """Нечётная длина, пример из main"""
        items = [5, 8, 1, 4, -7, 6, 12, 19, -6]
        expected = [-7, -6, 1, 4, 5, 6, 8, 12, 19]
        self.assertEqual(recursive_sort(items), expected)

    def test_sorted(self):
        """Уже упорядоченный список"""
        self.assertEqual(recursive_sort([1, 2, 3, 4]), [1, 2, 3, 4])

    def test_reversed(self):
        """Список в обратном порядке"""
        self.assertEqual(recursive_sort([4, 3, 2, 1]), [1, 2, 3, 4])

    def test_duplicates(self):
        """Повторяющиеся элементы"""
        self.assertEqual(recursive_sort([3, 1, 3, 2, 1]), [1, 1, 2, 3, 3])

    def test_int_and_float(self):
        """Целые и дробные числа вместе"""
        self.assertEqual(recursive_sort([2.5, 1, -0.5, 2]), [-0.5, 1, 2, 2.5])

    def test_strings(self):
        """Строки"""
        items = ["груша", "арбуз", "вишня"]
        self.assertEqual(recursive_sort(items), ["арбуз", "вишня", "груша"])

    def test_objects(self):
        """Объекты класса, у которого есть только операция <"""
        cards = [Card(3, "c"), Card(1, "a"), Card(2, "b")]
        names = [card.name for card in recursive_sort(cards)]
        self.assertEqual(names, ["a", "b", "c"])

    def test_stable(self):
        """Равные элементы остаются в исходном порядке"""
        cards = [Card(2, "first"), Card(1, "x"), Card(2, "second")]
        names = [card.name for card in recursive_sort(cards)]
        self.assertEqual(names, ["x", "first", "second"])

    def test_random(self):
        """Случайные списки разной длины сверяются с sorted"""
        random.seed(5)
        for length in range(50):
            items = [random.randint(-100, 100) for _ in range(length)]
            with self.subTest(items=items):
                self.assertEqual(recursive_sort(items), sorted(items))

    def test_original_not_changed(self):
        """Исходный список не изменяется"""
        items = [3, 1, 2]
        recursive_sort(items)
        self.assertEqual(items, [3, 1, 2])

    def test_new_list(self):
        """Результат всегда новый список, а не исходный"""
        for items in ([], [1], [1, 2], [2, 1]):
            with self.subTest(items=items):
                self.assertIsNot(recursive_sort(items), items)

    def test_not_list(self):
        """Набор не список"""
        with self.assertRaises(TypeError) as error:
            recursive_sort(1)
        self.assertEqual(str(error.exception), NOT_LIST)

    def test_other_collections(self):
        """Строка, кортеж, множество и None тоже не списки"""
        for value in ("21", (2, 1), {2, 1}, None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError) as error:
                    recursive_sort(value)
                self.assertEqual(str(error.exception), NOT_LIST)

    def test_not_comparable(self):
        """Элементы, которые нельзя сравнить операцией <"""
        for items in ([1, "a"], [3, None, 1], [None, None], [1, [2]]):
            with self.subTest(items=items):
                with self.assertRaises(TypeError) as error:
                    recursive_sort(items)
                self.assertEqual(str(error.exception), NOT_COMPARABLE)


if __name__ == "__main__":
    unittest.main()
