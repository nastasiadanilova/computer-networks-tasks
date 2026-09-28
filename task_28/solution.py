import heapq
from collections import deque

WEIGHTS = {"voice": 4, "video": 3, "data": 2, "bulk": 1}

class QoSScheduler:
    def __init__(self, mode: str):
        if mode not in ("PQ", "WFQ"):
            raise ValueError("mode must be PQ or WFQ")
        self._mode = mode
        self._heap = []          # для PQ
        self._queues = {c: deque() for c in WEIGHTS}  # для WFQ
        self._seq = 0

    def enqueue(self, pkt: dict):
        self._seq += 1
        p = dict(pkt, _seq=self._seq)
        if self._mode == "PQ":
            heapq.heappush(self._heap, (-pkt["priority"], self._seq, p))
        else:
            cls = pkt.get("class", "bulk")
            self._queues.get(cls, self._queues["bulk"]).append(p)

    def dequeue_all(self) -> list:
        result = []
        counter = 1
        if self._mode == "PQ":
            while self._heap:
                _, _, pkt = heapq.heappop(self._heap)
                pkt["served_at"] = counter
                counter += 1
                result.append(pkt)
        else:
            # WFQ: round-robin с весами
            order = []
            for cls, w in WEIGHTS.items():
                order.extend([cls] * w)  # 10-слотный цикл
            slot = 0
            total = sum(len(q) for q in self._queues.values())
            while total > 0:
                cls = order[slot % len(order)]
                slot += 1
                if self._queues[cls]:
                    pkt = self._queues[cls].popleft()
                    pkt["served_at"] = counter
                    counter += 1
                    result.append(pkt)
                    total -= 1
        # убираем служебное поле
        for p in result:
            p.pop("_seq", None)
        return result

if __name__ == "__main__":
    pkts = [
        {"id":1,"priority":1,"size_bytes":1400,"class":"bulk"},
        {"id":2,"priority":4,"size_bytes":200, "class":"voice"},
        {"id":3,"priority":3,"size_bytes":800, "class":"video"},
        {"id":4,"priority":2,"size_bytes":500, "class":"data"},
    ]
    pq = QoSScheduler("PQ")
    for p in pkts: pq.enqueue(p)
    print("PQ order:")
    for p in pq.dequeue_all(): print(p["id"], p["served_at"])

    wfq = QoSScheduler("WFQ")
    for p in pkts: wfq.enqueue(p)
    print("WFQ order:")
    for p in wfq.dequeue_all(): print(p["id"], p["served_at"])
