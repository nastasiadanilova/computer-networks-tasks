# Задание 35. Симулятор маршрутизации по алгоритму Дейкстры (OSPF-подобный)

## Условие

Реализовать функцию `dijkstra(graph, source)`, которая вычисляет кратчайшие пути от узла-источника до всех остальных узлов в графе сети. Реализовать также `shortest_path(graph, src, dst)` для получения конкретного пути.
Файл: solution.py

## Функции

- `dijkstra(graph, source)` -> dict {"node": (distance, prev_node)}
- `shortest_path(graph, src, dst)` -> list[str] - узлы пути от src до dst

Граф задается как `{"node": {"neighbor": cost, ...}, ...}`

## Пример вызова

```python
from solution import dijkstra, shortest_path

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
```

## Ожидаемый вывод

```
  R1: distance=0, via=None
  R2: distance=1, via=R1
  R3: distance=3, via=R2
  R4: distance=4, via=R3
['R1', 'R2', 'R3', 'R4']
```

## Запуск

```bash
python3 solution.py
```
