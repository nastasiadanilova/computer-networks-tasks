# Задание 12. Калькулятор времени передачи и эффективности канала

## Условие

Напишите функцию channel_stats(file_mb, bandwidth_mbps, prop_delay_ms, packet_b, ack_b=40) -> dict
Считает полное время передачи с учетом ACK, Stop-and-Wait и окна.
Файл: solution.py
Возвращает: file_bytes, bandwidth_bps, prop_delay_s, packet_bytes, num_packets,
           t_transmit_s, t_packet_s, t_ack_s, rtt_s, t_stop_wait_s, efficiency_pct

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import channel_stats
s = channel_stats(file_mb=50, bandwidth_mbps=100,
                  prop_delay_ms=20, packet_b=1500)
for k,v in s.items():
    print(f"{k}: {v}")
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
