from collections import namedtuple
from enum import StrEnum

INF = float("inf")
NO_COIN = -1


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках"""

    COINS_NOT_LIST = "coins должен быть списком"
    AMOUNT_NOT_INT = "amount должен быть целым числом"
    WRONG_COINS = "coins должен быть непустым списком положительных целых чисел"
    WRONG_AMOUNT = "amount должен быть неотрицательным целым числом"
    NEGATIVE_COIN = "монеты не могут быть отрицательными или нулевыми"
    COIN_NOT_INT = "все монеты должны быть целыми числами"


Result = namedtuple("Result", ["count", "combination"])


def _validate_input(coins: object, amount: object) -> None:
    """Проверяет вход задачи о размене монет.

    :param coins: список положительных целых номиналов
    :param amount: неотрицательная сумма
    :raise TypeError: если coins не список либо amount или номинал не целое
    :raise ValueError: если список пуст, сумма отрицательная или номинал не больше 0
    """
    if not isinstance(coins, list):
        raise TypeError(ErrorMessages.COINS_NOT_LIST)
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise TypeError(ErrorMessages.AMOUNT_NOT_INT)
    if not coins:
        raise ValueError(ErrorMessages.WRONG_COINS)
    if amount < 0:
        raise ValueError(ErrorMessages.WRONG_AMOUNT)
    for coin in coins:
        if isinstance(coin, bool) or not isinstance(coin, int):
            raise TypeError(ErrorMessages.COIN_NOT_INT)
    for coin in coins:
        if coin <= 0:
            raise ValueError(ErrorMessages.NEGATIVE_COIN)


def _restore_combination(amount: int, last_coin: list[int]) -> list[int]:
    """Восстанавливает набор монет по массиву последних монет.

    :param amount: целевая сумма
    :param last_coin: last_coin[s] - монета, которой достигнут минимум для s
    :return: список номиналов с суммой amount
    """
    combination: list[int] = []
    current = amount
    while current > 0:
        coin = last_coin[current]
        if coin == NO_COIN:
            return []
        combination.append(coin)
        current -= coin
    return combination


def coin_change(coins: list[int], amount: int) -> Result:
    """Возвращает минимальное число монет и один такой набор номиналов

    :param coins: список положительных целых номиналов
    :param amount: неотрицательная сумма
    :raise TypeError: если coins не список либо amount или номинал не целое
    :raise ValueError: если список пуст, сумма отрицательная или номинал не больше 0
    :return: Result с полями count и combination либо Result(None, None)
    """
    _validate_input(coins, amount)

    min_count: list[float] = [INF] * (amount + 1)
    last_coin: list[int] = [NO_COIN] * (amount + 1)
    min_count[0] = 0

    for current in range(1, amount + 1):
        for coin in coins:
            if coin > current:
                continue
            previous = min_count[current - coin]
            if previous == INF:
                continue
            candidate = previous + 1
            if candidate < min_count[current]:
                min_count[current] = candidate
                last_coin[current] = coin

    if min_count[amount] == INF:
        return Result(None, None)

    count = int(min_count[amount])
    combination = _restore_combination(amount, last_coin)
    return Result(count, combination)


def main():
    coins = [1, 2, 5]
    amount = 13
    print(coin_change(coins, amount))


if __name__ == "__main__":
    main()
