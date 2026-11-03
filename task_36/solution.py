"""
Задание 36. Симулятор протокола RIP (Distance Vector).

Реализует алгоритм Беллмана-Форда через обмен таблицами маршрутизации.
Максимальная метрика (hop count infinity) = 16 (как в RIP v1/v2).
"""

RIP_INFINITY = 16


class RIPNetwork:
    """
    Симулятор RIP-сети.

    Каждый маршрутизатор хранит таблицу {dst: (cost, next_hop)}.
    На каждой итерации маршрутизаторы рассылают свои таблицы соседям,
    соседи обновляют маршруты по алгоритму Беллмана-Форда.
    """

    def __init__(self):
        self._links: dict = {}          # router -> {neighbor: cost}
        self._tables: dict = {}         # router -> {dst: (cost, next_hop)}

    def _ensure(self, router: str):
        if router not in self._links:
            self._links[router] = {}
            self._tables[router] = {router: (0, router)}

    def add_link(self, r1: str, r2: str, cost: int):
        """Добавляет двунаправленный линк между r1 и r2 с заданной стоимостью."""
        self._ensure(r1)
        self._ensure(r2)
        self._links[r1][r2] = cost
        self._links[r2][r1] = cost
        # Инициализируем прямые маршруты
        self._tables[r1][r2] = (cost, r2)
        self._tables[r2][r1] = (cost, r1)

    def run(self, max_iterations: int = 20) -> int:
        """
        Запускает итеративный обмен таблицами до сходимости.

        Returns:
            Количество итераций до сходимости.
        """
        for iteration in range(1, max_iterations + 1):
            changed = False
            # Каждый маршрутизатор рассылает свою таблицу соседям
            for router, neighbors in self._links.items():
                for neighbor, link_cost in neighbors.items():
                    # Сосед смотрит на маршруты через router
                    for dst, (cost_via_router, _) in self._tables[router].items():
                        new_cost = cost_via_router + link_cost
                        if new_cost >= RIP_INFINITY:
                            continue
                        current_cost, _ = self._tables[neighbor].get(dst, (RIP_INFINITY, None))
                        if new_cost < current_cost:
                            self._tables[neighbor][dst] = (new_cost, router)
                            changed = True

            if not changed:
                return iteration

        return max_iterations

    def table(self, router: str) -> dict:
        """Возвращает таблицу маршрутизации для маршрутизатора."""
        return dict(self._tables.get(router, {}))


if __name__ == "__main__":
    net = RIPNetwork()
    net.add_link("R1", "R2", 1)
    net.add_link("R2", "R3", 2)
    net.add_link("R1", "R3", 10)

    iters = net.run()
    print(f"Converged in {iters} iterations")
    for dst, (cost, hop) in sorted(net.table("R1").items()):
        print(f"  -> {dst}: cost={cost}, next_hop={hop}")
