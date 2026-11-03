"""
Задание 40. Анализатор топологии сети и остовное дерево.

Компоненты связности, MST алгоритмом Прима, точки сочленения (DFS).
"""

import heapq


class NetworkTopology:
    """
    Анализатор топологии сети.

    Граф хранится в виде списков смежности с весами ребер.
    """

    def __init__(self):
        # node -> [(neighbor, cost), ...]
        self._adj: dict = {}

    def _ensure(self, node: str):
        if node not in self._adj:
            self._adj[node] = []

    def add_link(self, r1: str, r2: str, cost: int):
        """Добавляет двунаправленное ребро."""
        self._ensure(r1)
        self._ensure(r2)
        self._adj[r1].append((r2, cost))
        self._adj[r2].append((r1, cost))

    def connected_components(self) -> list:
        """
        Находит компоненты связности через BFS.

        Returns:
            Список множеств, каждое - узлы одной компоненты.
        """
        visited = set()
        components = []

        for start in self._adj:
            if start in visited:
                continue
            component = set()
            queue = [start]
            while queue:
                node = queue.pop()
                if node in visited:
                    continue
                visited.add(node)
                component.add(node)
                for neighbor, _ in self._adj[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
            components.append(component)

        return components

    def mst(self) -> list:
        """
        Минимальное остовное дерево алгоритмом Прима.

        Returns:
            Список кортежей (r1, r2, cost), отсортированных по cost.
            Строится только для наибольшей компоненты связности.
        """
        if not self._adj:
            return []

        # Берем наибольшую компоненту
        components = self.connected_components()
        largest = max(components, key=len)

        start = next(iter(largest))
        in_mst = {start}
        # heap: (cost, from_node, to_node)
        heap = [(cost, start, nb) for nb, cost in self._adj[start]]
        heapq.heapify(heap)
        edges = []

        while heap and len(in_mst) < len(largest):
            cost, u, v = heapq.heappop(heap)
            if v in in_mst:
                continue
            in_mst.add(v)
            edges.append((u, v, cost))
            for neighbor, c in self._adj[v]:
                if neighbor not in in_mst:
                    heapq.heappush(heap, (c, v, neighbor))

        return sorted(edges, key=lambda e: e[2])

    def articulation_points(self) -> set:
        """
        Находит точки сочленения (мосты и критические узлы) через DFS.

        Использует алгоритм Тарьяна с массивами disc (время входа) и low.

        Returns:
            Множество имен критических узлов.
        """
        visited = set()
        disc = {}
        low = {}
        parent = {}
        ap = set()
        timer = [0]

        def dfs(u: str):
            visited.add(u)
            disc[u] = low[u] = timer[0]
            timer[0] += 1
            child_count = 0

            for v, _ in self._adj[u]:
                if v not in visited:
                    child_count += 1
                    parent[v] = u
                    dfs(v)
                    low[u] = min(low[u], low[v])
                    # u точка сочленения если:
                    # 1) u - корень DFS с >=2 детьми
                    if parent.get(u) is None and child_count > 1:
                        ap.add(u)
                    # 2) u не корень и low[v] >= disc[u]
                    if parent.get(u) is not None and low[v] >= disc[u]:
                        ap.add(u)
                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])

        for node in self._adj:
            if node not in visited:
                parent[node] = None
                dfs(node)

        return ap


if __name__ == "__main__":
    topo = NetworkTopology()
    topo.add_link("R1", "R2", 2)
    topo.add_link("R2", "R3", 3)
    topo.add_link("R1", "R3", 5)
    topo.add_link("R3", "R4", 1)
    topo.add_link("R5", "R6", 4)

    components = topo.connected_components()
    print("Components:", [sorted(c) for c in components])

    print("MST:")
    for r1, r2, cost in topo.mst():
        print(f"  {r1} -- {r2}: {cost}")

    print("Articulation points:", topo.articulation_points())
