import math
import unittest

from main import generate_permutations_iter, generate_permutations_rec


def _same_items(left, right):
    pending = list(right)
    for item in left:
        for index, candidate in enumerate(pending):
            if candidate == item:
                del pending[index]
                break
        else:
            return False
    return not pending


def _assert_all_permutations(test_case, permutations, elements):
    test_case.assertEqual(len(permutations), math.factorial(len(elements)))
    seen = []
    for permutation in permutations:
        test_case.assertIsInstance(permutation, list)
        test_case.assertTrue(_same_items(permutation, elements))
        snapshot = list(permutation)
        test_case.assertNotIn(snapshot, seen)
        seen.append(snapshot)


class TestPermutations(unittest.TestCase):
    """Публичные примеры генерации перестановок."""

    def test_two_letters(self):
        """Обе перестановки двух букв."""
        expected = [["a", "b"], ["b", "a"]]
        for function in (generate_permutations_rec, generate_permutations_iter):
            with self.subTest(function=function.__name__):
                self.assertTrue(_same_items(function(["a", "b"]), expected))

    def test_three_letters(self):
        """Все шесть перестановок трёх букв."""
        elements = ["a", "b", "c"]
        for function in (generate_permutations_rec, generate_permutations_iter):
            with self.subTest(function=function.__name__):
                _assert_all_permutations(self, function(elements), elements)


if __name__ == "__main__":
    unittest.main()
