from abc import ABC, abstractmethod
from collections import namedtuple

WEIGHTS = "Веса"
COSTS = "Стоимости"

LENGTHS_NOT_EQUAL = "Списки весов и стоимости разной длины"
NOT_INT_WEIGHT_LIMIT = "Ограничение вместимости рюкзака не является целым числом"
NOT_POS_WEIGHT_LIMIT = "Ограничение вместимости рюкзака меньше единицы"
LESS_WEIGHT_LIMIT = (
    "Ограничение вместимости рюкзака меньше чем минимальный вес предмета"
)
NOT_LIST = "{0} не являются списком"
EMPTY_LIST = "{0} являются пустым списком"
NOT_INT = "{0} содержат нецелое значение"
NOT_POS = "{0} содержат нулевое или отрицательное значение"

KnapsackSolution = namedtuple("KnapsackSolution", ["cost", "items"])


class KnapsackAbstractSolver(ABC):
    """Абстрактный класс для решения задачи о рюкзаке."""

    def __init__(self, weights: list[int], costs: list[int], weight_limit: int):
        """Создаёт объект для решения задачи о рюкзаке.

        :param weights: список весов предметов
        :param costs: список стоимостей предметов
        :param weight_limit: ограничение вместимости рюкзака
        :raise TypeError: если веса или стоимости не список целых либо
            ограничение вместимости не целое
        :raise ValueError: если список пуст, длины не совпадают, есть
            неположительное значение или вместимость меньше минимального веса
        """
        self._validate_params(weights, costs, weight_limit)
        self._weights = weights
        self._costs = costs
        self._weight_limit = weight_limit

    @property
    def item_cnt(self):
        """Возвращает количество предметов для рюкзака."""
        return len(self._weights)

    @property
    def weights(self):
        """Возвращает список весов предметов для рюкзака."""
        return self._weights

    @property
    def costs(self):
        """Возвращает список стоимостей предметов для рюкзака."""
        return self._costs

    @property
    def weight_limit(self):
        """Возвращает ограничение вместимости рюкзака."""
        return self._weight_limit

    @abstractmethod
    def get_knapsack(self) -> KnapsackSolution:
        """Возвращает решение: cost — стоимость набора, items — индексы
        выбранных предметов (с нуля).
        """
        pass

    def get_weight(self, selected_items: list[bool]) -> int:
        """Возвращает суммарный вес выбранных предметов.

        :param selected_items: для каждого предмета True, если он в наборе
        """
        total_weight = 0
        for item_idx in range(self.item_cnt):
            if selected_items[item_idx]:
                total_weight += self._weights[item_idx]

        return total_weight

    def get_cost(self, selected_items: list[bool]) -> int:
        """Возвращает суммарную стоимость выбранных предметов.

        Если набор тяжелее вместимости, возвращает 0.

        :param selected_items: для каждого предмета True, если он в наборе
        """
        if self.get_weight(selected_items) > self._weight_limit:
            return 0

        total_cost = 0
        for item_idx in range(self.item_cnt):
            if selected_items[item_idx]:
                total_cost += self._costs[item_idx]

        return total_cost

    def _validate_params(
        self, weights: list[int], costs: list[int], weight_limit: int
    ) -> None:
        """Проверяет входные данные задачи о рюкзаке."""
        self._validate_list(weights, WEIGHTS)
        self._validate_list(costs, COSTS)

        if len(weights) != len(costs):
            raise ValueError(LENGTHS_NOT_EQUAL)

        if not isinstance(weight_limit, int) or isinstance(weight_limit, bool):
            raise TypeError(NOT_INT_WEIGHT_LIMIT)
        if weight_limit < 1:
            raise ValueError(NOT_POS_WEIGHT_LIMIT)
        if weight_limit < min(weights):
            raise ValueError(LESS_WEIGHT_LIMIT)

    def _validate_list(self, items: list[int], list_name: str) -> None:
        """Проверяет список весов или стоимостей."""
        if not isinstance(items, list):
            raise TypeError(NOT_LIST.format(list_name))
        if len(items) == 0:
            raise ValueError(EMPTY_LIST.format(list_name))

        for value in items:
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(NOT_INT.format(list_name))

        for value in items:
            if value <= 0:
                raise ValueError(NOT_POS.format(list_name))
