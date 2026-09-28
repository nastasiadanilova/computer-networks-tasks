# Задание 24. Симулятор Token Ring

## Условие

Класс Token Ring симулирует передачу маркера по кольцу.
Файл: solution.py Конструктор Token Ring(stations: list[str])Методы
• send(src, dst, data) -> list[str] - список событий передачи

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import TokenRing
ring = TokenRing(["A","B","C","D"])
for e in ring.send("A","C","hello"):
    print(e)
```

## Ожидаемый вывод

```
[TOKEN] A -> B
[TOKEN] B -> C
[DELIVER] C received 'hello' from A
[TOKEN] C -> D
[TOKEN] D -> A
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
