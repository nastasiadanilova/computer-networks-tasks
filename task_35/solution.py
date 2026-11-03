"""
Задание 35. Симулятор маршрутизации по алгоритму Дейкстры (OSPF-подобный).

Вычисляет кратчайшие пути в графе маршрутизаторов с весовыми ребрами.
"""

import heapq


def dijkstra(graph: dict, source: str) -> dict:
    """
    Алгоритм Дейкстры для поиска кратчайших путей от source до всех узлов.

    Args:
        graph: {"node": {"neighbor": cost, ...}, ...}
        source: стартовый узел

    Returns:
        {"node": (distance, prev_node)} - prev_node=None для source
    """
    # Инициализация: бесконечные расстояния до всех узлов
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0

    # Минимальная куча: (distance, node)
    heap = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue   # устаревший элемент кучи

        for neighbor, cost in graph[u].items():
            alt = dist[u] + cost
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = u
                heapq.heappush(heap, (alt, neighbor))

    return {node: (dist[node], prev[node]) for node in graph}


def shortest_path(graph: dict, src: str, dst: str) -> list:
    """
    Возвращает список узлов кратчайшего пути от src до dst.

    Returns:
        Список узлов включая src и dst, или [] если путь недостижим.
    """
    result = dijkstra(graph, src)
    if result[dst][0] == float("inf"):
        return []

    path = []
    node = dst
    while node is not None:
        path.append(node)
        node = result[node][1]

    path.reverse()
    return path


if __name__ == "__main__":
    network = {
        "R1": {"R2": 1, "R3": 4},
        "R2": {"R1": 1, "R3": 2, "R4": 5},
        "R3": {"R1": 4, "R2": 2, "R4": 1},
        "R4": {"R2": 5, "R3": 1},
    }

    result = dijkstra(network, "R1")
    for node, (dist, prev) in sorted(result.items()):
        print(f"  {node}: distance={dist}, via={prev}")

    print(shortest_path(network, "R1", "R4"))
