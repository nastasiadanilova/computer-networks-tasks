# Задание 22. Симулятор протокола скользящего окна (Go-Back-N)

## Условие

Класс Go-Back-N симулирует протокол Go-Back-N без реальной сети.
Файл: solution.py Параметры конструктора
• window_size - размер окна (int)
• loss_rate - вероятность потери пакета (0.0-1.0)
• seed - random seed Методы
• send(packets: list[str]) -> dict - симулировать отправку, вернуть статистику Возвращает{"sent": 10, "acked": 10, "retransmitted": 3, "rounds": 4}

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import GoBackN
gbn = GoBackN(window_size=4, loss_rate=0.3, seed=42)
stats = gbn.send(["pkt"+str(i) for i in range(10)])
print(stats)
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
