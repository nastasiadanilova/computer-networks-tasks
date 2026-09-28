# Задание 28. Симулятор QoS-очередей (Priority Queue / WFQ)

## Условие

Класс QoSScheduler симулирует два режима планировщика пакетов.
Файл: solution.py Конструктор QoSScheduler(mode: str) - "PQ" (Priority Queue) или "WFQ" (Weighted Fair Queue)Методы
• enqueue(pkt: dict) - {"id":1, "priority":1..4, "size_bytes":1400, "class":"voice"\|"video"\|"data"\|"bulk"}
• dequeue_all() -> list[dict] - вернуть пакеты в порядке обслуживания с полем "served_at": <порядковый номер>Логика PQОбслуживает строго по убыванию priority (4 = highest).Логика WFQВеса классов: voice=40%, video=30%, data=20%, bulk=10%.Round-robin по классам пропорционально весам (на каждые 10 пакетов: voice 4, video 3, data 2, bulk 1).

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import QoSScheduler
pkts = [
    {"id":1,"priority":1,"size_bytes":1400,"class":"bulk"},
    {"id":2,"priority":4,"size_bytes":200, "class":"voice"},
    {"id":3,"priority":3,"size_bytes":800, "class":"video"},
    {"id":4,"priority":2,"size_bytes":500, "class":"data"},
]
pq = QoSScheduler("PQ")
for p in pkts: pq.enqueue(p)
for p in pq.dequeue_all(): print(p["id"], p["served_at"])
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
