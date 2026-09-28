class TokenRing:
    def __init__(self, stations: list):
        self._ring = stations

    def send(self, src: str, dst: str, data: str) -> list:
        if src not in self._ring or dst not in self._ring:
            raise ValueError("Unknown station")
        n = len(self._ring)
        src_i = self._ring.index(src)
        events = []
        # Pass token around the ring
        for step in range(1, n + 1):
            cur = self._ring[(src_i + step) % n]
            prev = self._ring[(src_i + step - 1) % n]
            events.append(f"[TOKEN] {prev} -> {cur}")
            if cur == dst:
                events.append(f"[DELIVER] {dst} received {data!r} from {src}")
        return events

if __name__ == "__main__":
    ring = TokenRing(["A","B","C","D"])
    for e in ring.send("A","C","hello"):
        print(e)
