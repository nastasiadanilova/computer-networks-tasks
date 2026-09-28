import heapq

def shortest_path(graph: dict, src: str, dst: str) -> dict:
    dist = {n: float("inf") for n in graph}
    dist[src] = 0
    prev = {}
    heap = [(0, src)]
    while heap:
        cost, u = heapq.heappop(heap)
        if cost > dist[u]:
            continue
        for v, w in graph.get(u, {}).items():
            nc = dist[u] + w
            if nc < dist[v]:
                dist[v] = nc
                prev[v] = u
                heapq.heappush(heap, (nc, v))
    if dist[dst] == float("inf"):
        raise ValueError(f"No path from {src} to {dst}")
    path, cur = [], dst
    while cur in prev:
        path.append(cur); cur = prev[cur]
    path.append(src)
    path.reverse()
    return {"path": path, "cost": dist[dst], "hops": len(path)-1}

if __name__ == "__main__":
    graph = {
        "R1": {"R2": 10, "R3": 5},
        "R2": {"R1": 10, "R4": 3},
        "R3": {"R1": 5,  "R2": 3, "R4": 8},
        "R4": {"R2": 3,  "R3": 8},
    }
    print(shortest_path(graph, "R1", "R4"))
