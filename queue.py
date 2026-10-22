class Queue:
    """Структура данных Очередь"""

    def __init__(self):
        """Создаёт пустую очередь."""
        pass

    def is_empty(self) -> bool:
        """Возвращает True, если очередь пуста."""
        pass

    def __len__(self) -> int:
        """Возвращает число элементов."""
        pass

    def enqueue(self, value):
        """Ставит элемент в конец очереди.

        :param value: новое значение
        """
        pass

    def dequeue(self):
        """Удаляет и возвращает элемент из начала очереди.

        :raises IndexError: очередь пуста
        :return: удалённое значение
        """
        pass

    def peek(self):
        """Возвращает начало очереди, не удаляя его.

        :raises IndexError: очередь пуста
        :return: значение в начале
        """
        pass
