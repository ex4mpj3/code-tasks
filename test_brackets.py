import unittest

from main import is_brackets_balanced


class TestBrackets(unittest.TestCase):
    """Публичные примеры проверки скобок."""

    def test_balanced_expression(self):
        """Скобки в арифметическом выражении согласованы."""
        self.assertTrue(is_brackets_balanced("3 + 2 * (5 - [4 / {2 + 1}])"))

    def test_extra_closing(self):
        """Лишняя закрывающая скобка."""
        self.assertFalse(is_brackets_balanced("(]"))


if __name__ == "__main__":
    unittest.main()
