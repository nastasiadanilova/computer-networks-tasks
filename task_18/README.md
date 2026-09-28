# Задание 18. Симулятор выборов Root Bridge (STP)

## Условие

Функция elect_root(bridges: list[dict]) -> dict симулирует выборы Root Bridge
по протоколу STP (Spanning Tree Protocol).
Входные данные: [{"id": "SW1", "priority": 32768, "mac": "aa:bb:cc:dd:ee:01"}, ...]
Алгоритм: побеждает мост с наименьшим Bridge ID = (priority, mac).
Возвращает: {"root": {...}, "bridge_ids": [("SW1", "32768:aa:bb:cc:dd:ee:01"), ...]}

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import elect_root
bridges = [
  {"id":"SW1","priority":32768,"mac":"aa:bb:cc:dd:ee:01"},
  {"id":"SW2","priority":4096, "mac":"aa:bb:cc:dd:ee:02"},
  {"id":"SW3","priority":32768,"mac":"aa:bb:cc:dd:ee:03"},
]
print(elect_root(bridges))
```

## Ожидаемый вывод

```
{
  'root': {'id': 'SW2', 'priority': 4096, 'mac': 'aa:bb:cc:dd:ee:02'},
  'bridge_ids': [('SW1','32768:aa:bb:cc:dd:ee:01'),
                 ('SW2','4096:aa:bb:cc:dd:ee:02'),
                 ('SW3','32768:aa:bb:cc:dd:ee:03')]
}
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
