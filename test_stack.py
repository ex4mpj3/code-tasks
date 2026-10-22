import unittest

from stack import Stack


class TestStack(unittest.TestCase):
    """Публичные примеры стека."""

    def test_lifo(self):
        """Последний положенный элемент снимается первым."""
        stack = Stack()
        self.assertTrue(stack.is_empty())
        self.assertEqual(len(stack), 0)
        stack.push(1)
        stack.push(2)
        self.assertFalse(stack.is_empty())
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack.peek(), 2)
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.peek(), 1)
        self.assertEqual(stack.pop(), 1)
        self.assertTrue(stack.is_empty())

    def test_empty_stack(self):
        """У пустого стека нет вершины."""
        stack = Stack()
        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.peek()


if __name__ == "__main__":
    unittest.main()
