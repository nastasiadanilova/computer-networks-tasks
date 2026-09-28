import random

class GoBackN:
    def __init__(self, window_size: int, loss_rate: float = 0.0, seed: int = 0):
        self._ws = window_size
        self._loss = loss_rate
        self._rng = random.Random(seed)

    def send(self, packets: list) -> dict:
        n = len(packets)
        base = 0
        sent_total = 0
        retransmit = 0
        rounds = 0
        acked = [False] * n
        while base < n:
            rounds += 1
            window = list(range(base, min(base + self._ws, n)))
            all_acked = True
            for i in window:
                sent_total += 1
                lost = self._rng.random() < self._loss
                if not lost:
                    acked[i] = True
                else:
                    all_acked = False
            # advance base to first unacked
            while base < n and acked[base]:
                base += 1
            if not all_acked:
                # retransmit from base
                retransmit += len(list(range(base, min(base + self._ws, n))))
        return {"sent": sent_total, "acked": sum(acked),
                "retransmitted": retransmit, "rounds": rounds}

if __name__ == "__main__":
    gbn = GoBackN(window_size=4, loss_rate=0.3, seed=42)
    print(gbn.send(["pkt"+str(i) for i in range(10)]))
