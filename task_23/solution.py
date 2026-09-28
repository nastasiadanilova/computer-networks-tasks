import random

class CSMAChannel:
    def transmit(self, stations: list, seed: int = 0) -> dict:
        rng = random.Random(seed)
        queue = list(stations)
        collisions = 0; rounds = 0
        attempts = {s: 0 for s in stations}
        while len(queue) > 1:
            rounds += 1
            trying = list(queue)
            for s in trying:
                attempts[s] += 1
            if len(trying) > 1:
                collisions += 1
                # exponential backoff: каждый с вероятностью 0.5 отступает
                queue = [s for s in trying if rng.random() > 0.5]
                if not queue:
                    queue = list(trying)
        rounds += 1
        winner = queue[0]
        attempts[winner] = attempts.get(winner, 0) + 1
        return {"rounds": rounds, "collisions": collisions,
                "winner": winner, "attempts": attempts}

if __name__ == "__main__":
    ch = CSMAChannel()
    print(ch.transmit(["A","B","C"], seed=7))
