"""
Задание 47. Симулятор распределенной хеш-таблицы (кольцо Chord).

Реализует базовые операции Chord DHT: join, leave, lookup ответственного узла,
store/get данных. Узлы расположены на кольце [0, 2^m).
"""

import hashlib
import bisect


class ChordRing:
    """
    Симулятор кольца Chord (DHT).

    Узлы расположены на кольце целых чисел [0, 2^m).
    Ключи хешируются SHA-1 и усекаются до m бит.
    Ответственный узел - первый узел >= hash(key) по кольцу (successor).
    """

    def __init__(self, m: int = 8):
        self.m = m
        self.ring_size = 2 ** m
        self._sorted_nodes: list = []       # отсортированный список ID узлов
        self._node_data: dict = {}          # node_id -> {key: value} (хранилище)

    @property
    def nodes(self) -> list:
        """Список всех ID узлов в кольце."""
        return list(self._sorted_nodes)

    def _hash(self, key: str) -> int:
        """Хеширует ключ в пространство [0, ring_size)."""
        digest = hashlib.sha1(key.encode()).digest()
        return int.from_bytes(digest[:4], "big") % self.ring_size

    def join(self, node_id: int):
        """Добавляет узел с заданным ID в кольцо."""
        if node_id in self._node_data:
            return   # уже в кольце
        bisect.insort(self._sorted_nodes, node_id)
        self._node_data[node_id] = {}

    def leave(self, node_id: int):
        """Удаляет узел из кольца. Данные теряются (simplified)."""
        if node_id not in self._node_data:
            return
        self._sorted_nodes.remove(node_id)
        del self._node_data[node_id]

    def responsible(self, key_hash: int) -> int:
        """
        Находит узел, ответственный за данный хеш ключа (successor).

        Successor - первый узел на кольце, чей ID >= key_hash.
        Если такого нет - wrap-around к первому узлу.

        Args:
            key_hash: хеш ключа в диапазоне [0, ring_size)

        Returns:
            ID ответственного узла.

        Raises:
            RuntimeError: кольцо пустое.
        """
        if not self._sorted_nodes:
            raise RuntimeError("Кольцо Chord пустое")
        idx = bisect.bisect_left(self._sorted_nodes, key_hash)
        # wrap-around: если хеш больше всех узлов, возвращаем первый
        return self._sorted_nodes[idx % len(self._sorted_nodes)]

    def store(self, key: str, value):
        """Сохраняет значение на ответственном узле."""
        h = self._hash(key)
        node = self.responsible(h)
        self._node_data[node][key] = value

    def get(self, key: str):
        """
        Получает значение с ответственного узла.

        Returns:
            Значение или None, если ключ не найден.
        """
        h = self._hash(key)
        node = self.responsible(h)
        return self._node_data[node].get(key)

    def debug_info(self) -> str:
        """Возвращает отладочную информацию о кольце."""
        lines = [f"Chord ring (m={self.m}, size={self.ring_size})"]
        for node in self._sorted_nodes:
            data = self._node_data[node]
            lines.append(f"  Node {node:3d}: {len(data)} keys stored")
        return "\n".join(lines)


if __name__ == "__main__":
    ring = ChordRing(m=8)
    for node in [10, 50, 100, 200]:
        ring.join(node)

    print("Nodes:", sorted(ring.nodes))
    print("Responsible for key 30:", ring.responsible(30))
    print("Responsible for key 75:", ring.responsible(75))

    ring.store("hostname", "router-01")
    print("get hostname:", ring.get("hostname"))
