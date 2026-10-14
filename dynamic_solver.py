from knapsack_abs_solver import KnapsackAbstractSolver, KnapsackSolution


class DynamicSolver(KnapsackAbstractSolver):
    """Решение задачи о рюкзаке динамическим программированием."""

    def get_knapsack(self) -> KnapsackSolution:
        """Возвращает набор максимальной стоимости, не тяжелее вместимости."""
        max_costs = self._build_max_costs()
        selected_items = self._recover_selection(max_costs)

        items = []
        for item_idx in range(self.item_cnt):
            if selected_items[item_idx]:
                items.append(item_idx)

        return KnapsackSolution(self.get_cost(selected_items), items)

    def _build_max_costs(self) -> list[list[int]]:
        """Возвращает таблицу F: F[i][w] — максимальная стоимость
        при первых i предметах и вместимости w.
        """
        max_costs = []
        for _ in range(self.item_cnt + 1):
            max_costs.append([0] * (self.weight_limit + 1))

        for item_num in range(1, self.item_cnt + 1):
            item_weight = self.weights[item_num - 1]
            item_cost = self.costs[item_num - 1]
            for capacity in range(1, self.weight_limit + 1):
                without_item = max_costs[item_num - 1][capacity]
                if item_weight > capacity:
                    max_costs[item_num][capacity] = without_item
                else:
                    with_item = max_costs[item_num - 1][capacity - item_weight]
                    max_costs[item_num][capacity] = max(
                        without_item, with_item + item_cost
                    )

        return max_costs

    def _recover_selection(self, max_costs: list[list[int]]) -> list[bool]:
        """Восстанавливает по таблице, какие предметы взяты в набор."""
        selected_items = [False] * self.item_cnt
        capacity = self.weight_limit

        for item_num in range(self.item_cnt, 0, -1):
            if max_costs[item_num][capacity] != max_costs[item_num - 1][capacity]:
                selected_items[item_num - 1] = True
                capacity -= self.weights[item_num - 1]

        return selected_items
