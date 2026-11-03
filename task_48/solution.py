"""
Задание 48. Симулятор протокола AODV (реактивная маршрутизация).

AODV: Route Request (RREQ) рассылается широковещательно, маршрут строится
через цепочку обратных указателей. Используется BFS для поиска кратчайшего пути.
"""

from collections import deque


class AODVNetwork:
    """
    Симулятор AODV-сети.

    Топология хранится как граф смежности. При запросе маршрута выполняется
    RREQ-флуд (BFS), после чего RREP прокладывает обратный путь.
    Найденные маршруты кешируются в таблицах маршрутизации узлов.
    """

    def __init__(self):
        self._adj: dict = {}               # node -> set of neighbors
        self._route_tables: dict = {}      # node -> {dst: {next_hop, hops}}
        self._seq: dict = {}              # node -> sequence number

    def _ensure(self, node: str):
        if node not in self._adj:
            self._adj[node] = set()
            self._route_tables[node] = {}
            self._seq[node] = 0

    def add_link(self, n1: str, n2: str):
        """Добавляет двунаправленный беспроводной линк."""
        self._ensure(n1)
        self._ensure(n2)
        self._adj[n1].add(n2)
        self._adj[n2].add(n1)

    def route_discovery(self, src: str, dst: str) -> list:
        """
        Запускает процедуру обнаружения маршрута RREQ/RREP.

        Использует BFS (имитация RREQ-флуда) для нахождения кратчайшего пути.
        После нахождения пути обновляет таблицы маршрутизации всех промежуточных узлов.

        Returns:
            Список узлов маршрута от src до dst, или [] если пути нет.
        """
        if src not in self._adj or dst not in self._adj:
            return []

        # BFS: ищем кратчайший путь
        queue = deque([[src]])
        visited = {src}

        best_path = None
        while queue:
            path = queue.popleft()
            current = path[-1]

            if current == dst:
                best_path = path
                break

            for neighbor in self._adj[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

        if best_path is None:
            return []

        # RREP: обновляем таблицы маршрутов вдоль пути (от dst к src)
        for i, node in enumerate(best_path):
            remaining = best_path[i:]   # оставшийся путь от этого узла до dst
            if len(remaining) > 1:
                next_hop = remaining[1]
                hops = len(remaining) - 1
                self._route_tables[node][dst] = {
                    "next_hop": next_hop,
                    "hops": hops,
                }
            # Также добавляем обратные маршруты к src
            preceding = best_path[:i + 1]
            if i > 0:
                prev_node = preceding[-2]
                hops_back = i
                self._route_tables[node][src] = {
                    "next_hop": prev_node,
                    "hops": hops_back,
                }

        self._seq[src] += 1
        return best_path

    def routing_table(self, node: str) -> dict:
        """Возвращает таблицу маршрутов для узла."""
        return dict(self._route_tables.get(node, {}))


if __name__ == "__main__":
    net = AODVNetwork()
    net.add_link("A", "B")
    net.add_link("B", "C")
    net.add_link("C", "D")
    net.add_link("A", "C")

    path = net.route_discovery("A", "D")
    print("Path A->D:", path)

    path2 = net.route_discovery("A", "C")
    print("Path A->C:", path2)

    print("A routing table:", net.routing_table("A"))
