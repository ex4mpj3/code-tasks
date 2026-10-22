import unittest
from queue import Queue


class TestQueue(unittest.TestCase):
    """Публичные примеры очереди."""

    def test_fifo(self):
        """Первый поставленный элемент выходит первым."""
        queue = Queue()
        self.assertTrue(queue.is_empty())
        self.assertEqual(len(queue), 0)
        queue.enqueue(1)
        queue.enqueue(2)
        self.assertFalse(queue.is_empty())
        self.assertEqual(len(queue), 2)
        self.assertEqual(queue.peek(), 1)
        self.assertEqual(len(queue), 2)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.peek(), 2)
        self.assertEqual(queue.dequeue(), 2)
        self.assertTrue(queue.is_empty())

    def test_empty_queue(self):
        """У пустой очереди нет начала."""
        queue = Queue()
        with self.assertRaises(IndexError):
            queue.dequeue()
        with self.assertRaises(IndexError):
            queue.peek()


if __name__ == "__main__":
    unittest.main()
