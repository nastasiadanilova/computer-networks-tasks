# Задание 34. Симулятор TCP-контроля перегрузки (Tahoe)

## Условие

Реализовать класс `TCPTahoe`, симулирующий алгоритм контроля перегрузки TCP Tahoe: slow start, congestion avoidance, fast retransmit. Симуляция работает пораундово (по RTT).
Файл: solution.py

## Класс TCPTahoe

- `__init__(ssthresh=64)` - начальный порог slow start
- `step(loss=False)` -> int - выполняет один раунд, возвращает cwnd
- `cwnd` - текущее окно перегрузки (в сегментах)
- `ssthresh` - текущий порог
- `phase` - "slow_start" или "congestion_avoidance"

## Пример вызова

```python
from solution import TCPTahoe

tcp = TCPTahoe(ssthresh=8)
for rtt in range(12):
    loss = (rtt == 6)
    cwnd = tcp.step(loss=loss)
    print(f"RTT {rtt:2d}: cwnd={cwnd:3d}, ssthresh={tcp.ssthresh}, phase={tcp.phase}")
```

## Ожидаемый вывод

```
RTT  0: cwnd=  2, ssthresh=8, phase=slow_start
RTT  1: cwnd=  4, ssthresh=8, phase=slow_start
RTT  2: cwnd=  8, ssthresh=8, phase=congestion_avoidance
RTT  3: cwnd=  9, ssthresh=8, phase=congestion_avoidance
RTT  4: cwnd= 10, ssthresh=8, phase=congestion_avoidance
RTT  5: cwnd= 11, ssthresh=8, phase=congestion_avoidance
RTT  6: cwnd=  1, ssthresh=5, phase=slow_start
RTT  7: cwnd=  2, ssthresh=5, phase=slow_start
RTT  8: cwnd=  4, ssthresh=5, phase=slow_start
RTT  9: cwnd=  5, ssthresh=5, phase=congestion_avoidance
RTT 10: cwnd=  6, ssthresh=5, phase=congestion_avoidance
RTT 11: cwnd=  7, ssthresh=5, phase=congestion_avoidance
```

## Запуск

```bash
python3 solution.py
```
