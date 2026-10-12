from collections import namedtuple
from enum import StrEnum

INF = float("inf")


class ErrorMessages(StrEnum):
    """Перечисление сообщений об ошибках"""

    COINS_NOT_LIST = "coins должен быть списком"
    AMOUNT_NOT_INT = "amount должен быть целым числом"
    WRONG_COINS = "coins должен быть непустым списком положительных целых чисел"
    WRONG_AMOUNT = "amount должен быть неотрицательным целым числом"
    NEGATIVE_COIN = "монеты не могут быть отрицательными или нулевыми"
    COIN_NOT_INT = "все монеты должны быть целыми числами"


Result = namedtuple("Result", ["count", "combination"])


def coin_change(coins: list[int], amount: int) -> Result:
    """Возвращает минимальное число монет и один такой набор номиналов

    :param coins: список положительных целых номиналов
    :param amount: неотрицательная сумма
    :raise TypeError: если coins не список либо amount или номинал не целое
    :raise ValueError: если список пуст, сумма отрицательная или номинал не больше 0
    :return: Result с полями count и combination либо Result(None, None)
    """
    pass


def main():
    coins = [1, 2, 5]
    amount = 13
    print(coin_change(coins, amount))


if __name__ == "__main__":
    main()
