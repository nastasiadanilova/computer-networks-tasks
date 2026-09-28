# Задание 21. Алгоритм Дейкстры для поиска кратчайшего пути в сети

## Условие

Функция shortest_path(graph: dict, src: str, dst: str) -> dict
Файл: solution.py
graph -- словарь смежности: {"R1": {"R2": 10, "R3": 5}, ...}
(веса = метрики маршрутов)
Возвращает: {"path": ["R1", "R3", "R2"], "cost": 15, "hops": 2}

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import shortest_path
graph = {
  "R1": {"R2": 10, "R3": 5},
  "R2": {"R1": 10, "R4": 3},
  "R3": {"R1": 5,  "R2": 3, "R4": 8},
  "R4": {"R2": 3,  "R3": 8},
}
print(shortest_path(graph, "R1", "R4"))
```

## Ожидаемый вывод

```
{'path': ['R1', 'R3', 'R2', 'R4'], 'cost': 11, 'hops': 3}
```

## Критерии приемки



## Запуск

```bash
python3 solution.py
```

Через Docker:
```bash
docker run --rm -v $(pwd):/app python:3.11-slim python3 /app/solution.py
```
