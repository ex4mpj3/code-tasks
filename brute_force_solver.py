from knapsack_abs_solver import KnapsackAbstractSolver, KnapsackSolution


class BruteForceSolver(KnapsackAbstractSolver):
    """Решение задачи о рюкзаке полным перебором подмножеств."""

    def get_knapsack(self) -> KnapsackSolution:
        """Возвращает набор максимальной стоимости, не тяжелее вместимости."""
        best_cost = 0
        best_selection = [False] * self.item_cnt

        for mask in range(1, 2**self.item_cnt):
            selected_items = []
            for item_idx in range(self.item_cnt):
                selected_items.append((mask >> item_idx) % 2 == 1)

            cost = self.get_cost(selected_items)
            if cost > best_cost:
                best_cost = cost
                best_selection = selected_items

        best_items = []
        for item_idx in range(self.item_cnt):
            if best_selection[item_idx]:
                best_items.append(item_idx)

        return KnapsackSolution(best_cost, best_items)
