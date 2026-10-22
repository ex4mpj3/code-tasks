import unittest
from queue import Queue

from main import rabbits


class TestRabbits(unittest.TestCase):
    """Публичные примеры задачи о кроликах."""

    def test_first_months(self):
        """До первой смерти численность совпадает с числами Фибоначчи."""
        self.assertEqual(rabbits(1, 2), 1)
        self.assertEqual(rabbits(2, 2), 1)
        self.assertEqual(rabbits(6, 8), 8)

    def test_first_death(self):
        """На 8-й месяц при жизни 7 месяцев остаётся 20 пар."""
        self.assertEqual(rabbits(8, 7), 20)

    def test_later_months(self):
        """Численность считается и после нескольких смертей."""
        self.assertEqual(rabbits(20, 7), 5266)
        self.assertEqual(rabbits(25, 7), 53515)


if __name__ == "__main__":
    unittest.main()
