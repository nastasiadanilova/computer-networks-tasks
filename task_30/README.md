# Задание 30. Симулятор traceroute

## Условие

Реализовать функцию `traceroute(destination, max_hops)`, которая симулирует работу утилиты traceroute: возвращает список переходов (hop) с TTL, условным IP-адресом и временем ответа.
Файл: solution.py

## Функции

- `traceroute(destination, max_hops=30)` -> list[dict]

Каждый элемент списка: `{"hop": int, "ip": str, "rtt_ms": float}`

## Пример вызова

```python
from solution import traceroute

hops = traceroute("8.8.8.8", max_hops=5)
for h in hops:
    print(f"  {h['hop']:2d}  {h['ip']:<18s}  {h['rtt_ms']:.2f} ms")
```

## Ожидаемый вывод

```
   1  192.168.1.1         0.45 ms
   2  10.0.0.1            5.12 ms
   3  172.16.0.1          12.38 ms
   4  8.8.8.8             20.74 ms
```

(конкретные IP и RTT зависят от среды выполнения или симуляции)

## Запуск

```bash
python3 solution.py
```
