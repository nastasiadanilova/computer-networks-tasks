# Задание 04. VLSM: распределение адресного пространства

## Условие

Функция vlsm_allocate(network: str, segments: list[tuple[str,int]]) -> list[dict]
распределяет IP-пространство по методу VLSM: от большего сегмента к меньшему.
Входные данные:
  network  - блок, например "10.0.0.0/20"
  segments - список [("Sales", 120), ("IT", 55), ("HR", 25), ("Link1", 2)]
  (порядок произвольный, функция сортирует сама по убыванию)
Структура элемента:
  {"name": "Sales", "required": 120, "allocated": "10.0.0.0/25",
   "first_host": "10.0.0.1", "last_host": "10.0.0.126", "usable": 126, "waste": 6}
  waste - разница между usable и required.

## Параметры

| | |
|---|---|
| Сигнатура | `vlsm_allocate(network: str, segments: list[tuple[str,int]]) -> list[dict]` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import vlsm_allocate
segs = [("Sales", 120), ("IT", 55), ("HR", 25), ("Link1", 2)]
for row in vlsm_allocate("10.0.0.0/20", segs):
    print(row)
```

## Ожидаемый вывод

```

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
