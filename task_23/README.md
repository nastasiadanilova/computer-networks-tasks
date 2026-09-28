# Задание 23. Симулятор коллизий CSMA/CD

## Условие

Класс CSMAChannel симулирует передачу в среде CSMA/CD.
Файл: solution.py Методы
• transmit(stations: list[str], seed=0) -> dict Симулирует попытки передачи N станций, возвращает:{"rounds": int, "collisions": int, "winner": str, "attempts": {station: count}}Алгоритм1. Все станции пытаются передать одновременно2. Если >1 - коллизия, случайная задержка (backoff), повтор3. Если 1 - она победила

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import CSMAChannel
ch = CSMAChannel()
print(ch.transmit(["A","B","C"], seed=7))
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
