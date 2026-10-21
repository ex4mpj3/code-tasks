import unittest

from main import ErrorMessages, Result, coin_change


def _assert_valid_change(test_case, coins, amount, result, expected_count):
    test_case.assertEqual(result.count, expected_count)
    test_case.assertEqual(len(result.combination), expected_count)
    test_case.assertEqual(sum(result.combination), amount)
    allowed = set(coins)
    for coin in result.combination:
        test_case.assertIn(coin, allowed)


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

    def test_bool_amount(self):
        """Логическое значение не является целой суммой"""
        with self.assertRaises(TypeError) as error:
            coin_change([1, 2, 5], True)
        self.assertEqual(str(error.exception), ErrorMessages.AMOUNT_NOT_INT)

    def test_bool_coin(self):
        """Логическое значение не является номиналом"""
        with self.assertRaises(TypeError) as error:
                coin_change([1, False, 5], 10)
        self.assertEqual(str(error.exception), ErrorMessages.COIN_NOT_INT)

    def test_greedy_not_optimal(self):
        """Оптимальный набор отличается от жадного решения"""
        coins = [1, 4, 6]
        result = coin_change(coins, 8)
        _assert_valid_change(self, coins, 8, result, 2)

    def test_no_one_coin(self):
        """Сумму можно оставить без номинала 1"""
        coins = [4, 6]
        result = coin_change(coins, 14)
        _assert_valid_change(self, coins, 14, result, 3)

    def test_zero_amount_invalid_coin(self):
        """Номиналы при нулевой сумме"""
        with self.assertRaises(ValueError) as error:
            coin_change([0], 0)
        self.assertEqual(str(error.exception), ErrorMessages.NEGATIVE_COIN)

    def test_smaller_than_all_coins(self):
        """Сумма меньше любого номинала"""
        self.assertEqual(coin_change([5, 7], 3), Result(None, None))


if __name__ == "__main__":
    unittest.main()
