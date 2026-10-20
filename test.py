import unittest
from collections import deque

from main import ErrorMessages, Result, coin_change


def _assert_valid_change(test_case, coins, amount, result, expected_count):
    test_case.assertEqual(result.count, expected_count)
    test_case.assertEqual(len(result.combination), expected_count)
    test_case.assertEqual(sum(result.combination), amount)
    allowed = set(coins)
    for coin in result.combination:
        test_case.assertIn(coin, allowed)


def _bfs_min_count(coins, amount):
    """Контрольный расчёт: минимальное число монет через BFS по суммам."""
    if amount == 0:
        return 0
    distance = [-1] * (amount + 1)
    distance[0] = 0
    queue = deque([0])
    while queue:
        current = queue.popleft()
        for coin in coins:
            next_sum = current + coin
            if next_sum <= amount and distance[next_sum] == -1:
                distance[next_sum] = distance[current] + 1
                queue.append(next_sum)
    return distance[amount] if distance[amount] != -1 else None


class TestCoinChange(unittest.TestCase):
    """Набор тестов размена монет"""

    def test_none_coins(self):
        """coins равен None"""
        with self.assertRaises(TypeError) as error:
            coin_change(None, 10)
        self.assertEqual(str(error.exception), ErrorMessages.COINS_NOT_LIST)

    def test_empty_coins(self):
        """Пустой список номиналов"""
        with self.assertRaises(ValueError) as error:
            coin_change([], 10)
        self.assertEqual(str(error.exception), ErrorMessages.WRONG_COINS)

    def test_none_amount(self):
        """amount равен None"""
        with self.assertRaises(TypeError) as error:
            coin_change([1, 2, 5], None)
        self.assertEqual(str(error.exception), ErrorMessages.AMOUNT_NOT_INT)

    def test_coin_not_int(self):
        """Номинал не целое"""
        with self.assertRaises(TypeError) as error:
            coin_change([1, 2.5, 5], 10)
        self.assertEqual(str(error.exception), ErrorMessages.COIN_NOT_INT)

    def test_negative_amount(self):
        """Отрицательная сумма"""
        with self.assertRaises(ValueError) as error:
            coin_change([1, 2, 5], -5)
        self.assertEqual(str(error.exception), ErrorMessages.WRONG_AMOUNT)

    def test_negative_coin(self):
        """Отрицательный номинал"""
        with self.assertRaises(ValueError) as error:
            coin_change([1, -2, 5], 10)
        self.assertEqual(str(error.exception), ErrorMessages.NEGATIVE_COIN)

    def test_zero_coin(self):
        """Нулевой номинал"""
        with self.assertRaises(ValueError) as error:
            coin_change([1, 0, 5], 10)
        self.assertEqual(str(error.exception), ErrorMessages.NEGATIVE_COIN)

    def test_impossible(self):
        """Сумму набрать нельзя"""
        self.assertEqual(coin_change([3, 7], 5), Result(None, None))

    def test_zero_amount(self):
        """Сумма 0"""
        self.assertEqual(coin_change([1, 2, 5], 0), Result(0, []))

    def test_single_coin(self):
        """Одна монета совпадает с суммой"""
        self.assertEqual(coin_change([1, 3, 7, 10], 7), Result(1, [7]))

    def test_basic(self):
        """Пример: 13 из 1, 2 и 5"""
        coins = [1, 2, 5]
        result = coin_change(coins, 13)
        _assert_valid_change(self, coins, 13, result, 4)

    def test_two_optima(self):
        """Несколько наборов из двух монет"""
        coins = [1, 3, 4]
        result = coin_change(coins, 6)
        _assert_valid_change(self, coins, 6, result, 2)

    def test_one_denomination(self):
        """Один номинал"""
        self.assertEqual(coin_change([2], 8), Result(4, [2, 2, 2, 2]))


class TestCoinChangeExtended(unittest.TestCase):
    """Дополнение команды: свойства, минимальность, краевые случаи"""

    def test_impossible_returns_none_fields(self):
        """У недостижимой суммы оба поля None"""
        result = coin_change([3, 7], 5)
        self.assertIsNone(result.count)
        self.assertIsNone(result.combination)

    def test_input_not_mutated(self):
        """Входной список не меняется"""
        coins = [1, 2, 5]
        original = coins[:]
        coin_change(coins, 13)
        self.assertEqual(coins, original)

    def test_amount_bool(self):
        """bool не считается целым"""
        with self.assertRaises(TypeError) as error:
            coin_change([1, 2, 5], True)
        self.assertEqual(str(error.exception), ErrorMessages.AMOUNT_NOT_INT)

    def test_amount_float(self):
        """Дробная сумма"""
        with self.assertRaises(TypeError) as error:
            coin_change([1, 2, 5], 10.0)
        self.assertEqual(str(error.exception), ErrorMessages.AMOUNT_NOT_INT)

    def test_coins_tuple(self):
        """Кортеж вместо списка"""
        with self.assertRaises(TypeError) as error:
            coin_change((1, 2, 5), 10)
        self.assertEqual(str(error.exception), ErrorMessages.COINS_NOT_LIST)

    def test_coin_bool(self):
        """bool среди монет"""
        with self.assertRaises(TypeError) as error:
            coin_change([1, True, 5], 10)
        self.assertEqual(str(error.exception), ErrorMessages.COIN_NOT_INT)

    def test_error_order(self):
        """TypeError нецелой монеты важнее ValueError отрицательной"""
        with self.assertRaises(TypeError) as error:
            coin_change([1, -2, "a"], 10)
        self.assertEqual(str(error.exception), ErrorMessages.COIN_NOT_INT)

    def test_against_bfs(self):
        """Сверка с BFS-эталоном на малых суммах"""
        coin_sets = ([1, 2, 5], [1, 3, 4], [2, 3, 7], [5], [3, 7], [1, 1, 2, 5])
        for coins in coin_sets:
            for amount in range(41):
                expected = _bfs_min_count(coins, amount)
                result = coin_change(list(coins), amount)
                with self.subTest(coins=coins, amount=amount):
                    if expected is None:
                        self.assertEqual(result, Result(None, None))
                    else:
                        _assert_valid_change(self, coins, amount, result, expected)

    def test_large_amount(self):
        """Большая сумма: 10 000 из 1, 2, 5"""
        coins = [1, 2, 5]
        result = coin_change(coins, 10_000)
        _assert_valid_change(self, coins, 10_000, result, 2_000)


if __name__ == "__main__":
    unittest.main()
