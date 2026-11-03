# Задание 49. Система обнаружения вторжений (IDS)

## Условие

Реализовать класс `NetworkIDS` - упрощенную систему обнаружения вторжений. IDS анализирует поток пакетов и выявляет аномалии: port scan, SYN flood, DNS amplification, повторяющиеся ICMP (ping flood).
Файл: solution.py

## Класс NetworkIDS

- `__init__(window_sec=60)` - временное окно для анализа
- `add_rule(name, condition_fn, threshold, description)` - добавляет правило
- `process_packet(packet)` - обрабатывает пакет (обновляет счетчики)
- `alerts()` -> list[dict] - список сгенерированных оповещений
- `stats()` -> dict - текущая статистика

Пакет: `{"ts": float, "src": str, "dst": str, "proto": str, "dst_port": int, "flags": str}`

## Пример вызова

```python
from solution import NetworkIDS
import time

ids = NetworkIDS(window_sec=60)

# Симулируем port scan: один IP обращается к множеству портов
base_ts = time.time()
for port in range(20, 40):
    ids.process_packet({
        "ts": base_ts, "src": "10.0.0.1", "dst": "192.168.1.1",
        "proto": "tcp", "dst_port": port, "flags": "SYN"
    })

alerts = ids.alerts()
for a in alerts:
    print(f"[{a['rule']}] {a['src']} -> {a['description']}")

print("Total packets:", ids.stats()["total_packets"])
```

## Ожидаемый вывод

```
[port_scan] 10.0.0.1 -> Port scan detected: 10 unique ports
Total packets: 20
```

## Запуск

```bash
python3 solution.py
```
