# Задание 40. Анализатор топологии сети и остовное дерево

## Условие

Реализовать класс `NetworkTopology` для анализа сетевого графа: поиск связных компонент, нахождение минимального остовного дерева (MST) алгоритмом Прима, определение критических узлов (точек сочленения).
Файл: solution.py

## Класс NetworkTopology

- `__init__()` - пустой граф
- `add_link(r1, r2, cost)` - добавляет ребро
- `connected_components()` -> list[set] - компоненты связности
- `mst()` -> list[(r1, r2, cost)] - минимальное остовное дерево (алгоритм Прима)
- `articulation_points()` -> set - точки сочленения (критические узлы)

## Пример вызова

```python
from solution import NetworkTopology

topo = NetworkTopology()
topo.add_link("R1", "R2", 2)
topo.add_link("R2", "R3", 3)
topo.add_link("R1", "R3", 5)
topo.add_link("R3", "R4", 1)
topo.add_link("R5", "R6", 4)  # отдельная компонента

print("Components:", topo.connected_components())
print("MST:")
for r1, r2, cost in topo.mst():
    print(f"  {r1} -- {r2}: {cost}")
print("Articulation points:", topo.articulation_points())
```

## Ожидаемый вывод

```
Components: [['R1', 'R2', 'R3', 'R4'], ['R5', 'R6']]
MST:
  R3 -- R4: 1
  R1 -- R2: 2
  R2 -- R3: 3
Articulation points: {'R3'}
```

## Запуск

```bash
python3 solution.py
```
