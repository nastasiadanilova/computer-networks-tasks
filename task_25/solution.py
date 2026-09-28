import copy

class RIPSimulator:
    def __init__(self, topology: dict):
        self._topo = topology
        self._nodes = list(topology.keys())
        self._conv = 0

    def run(self, max_iterations: int = 100) -> dict:
        # Init: каждый знает только себя и прямых соседей
        tables = {}
        for node in self._nodes:
            tables[node] = {n: float("inf") for n in self._nodes}
            tables[node][node] = 0
            for neighbor, cost in self._topo[node].items():
                tables[node][neighbor] = cost

        for iteration in range(1, max_iterations + 1):
            new_tables = copy.deepcopy(tables)
            changed = False
            for node in self._nodes:
                for neighbor, link_cost in self._topo[node].items():
                    for dst in self._nodes:
                        via_neighbor = tables[neighbor][dst]
                        if via_neighbor == float("inf"):
                            continue
                        new_cost = link_cost + via_neighbor
                        if new_cost < new_tables[node][dst]:
                            new_tables[node][dst] = new_cost
                            changed = True
            tables = new_tables
            if not changed:
                self._conv = iteration
                break
        # Заменяем inf на None для читаемости
        return {n: {d: (v if v != float("inf") else None)
                    for d, v in row.items()}
                for n, row in tables.items()}

    def converged_at(self) -> int:
        return self._conv

if __name__ == "__main__":
    import pprint
    topo = {
        "R1": {"R2": 1, "R3": 7},
        "R2": {"R1": 1, "R3": 2, "R4": 4},
        "R3": {"R1": 7, "R2": 2, "R4": 1},
        "R4": {"R2": 4, "R3": 1},
    }
    rip = RIPSimulator(topo)
    tables = rip.run()
    pprint.pprint(tables)
    print("Converged at iteration:", rip.converged_at())
