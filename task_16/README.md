# Задание 16. Анализатор лога сетевых пакетов

## Условие

Функция analyze_log(lines: list[str]) -> dict парсит текстовый лог пакетов
и выдает статистику трафика.
Файл: solution.py
Формат строки лога: 2026-09-01 10:00:01 TCP 192.168.1.10:54321 -> 8.8.8.8:443 len=1400
Возвращает: total_packets, total_bytes, by_proto, top_src, top_dst, top_dst_port

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import analyze_log
lines = [
  "2026-09-01 10:00:01 TCP 192.168.1.10:54321 -> 8.8.8.8:443 len=1400",
  "2026-09-01 10:00:02 TCP 192.168.1.10:54322 -> 8.8.8.8:443 len=1400",
  "2026-09-01 10:00:03 UDP 192.168.1.11:53001 -> 8.8.4.4:53  len=120",
  "2026-09-01 10:00:04 TCP 192.168.1.12:60001 -> 10.0.0.1:22 len=200",
]
import pprint; pprint.pprint(analyze_log(lines))
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
