# Задание 50. Симулятор SDN-контроллера (OpenFlow-подобный)

## Условие

Реализовать упрощенный SDN-контроллер с потоковой таблицей (flow table). Контроллер управляет коммутаторами: устанавливает правила (flow rules) и обрабатывает пакеты по принципу match-action. Поддерживать приоритеты правил и счетчики.
Файл: solution.py

## Классы

- `FlowRule(priority, match, action)` - правило потока
  - match: dict с полями для сопоставления (src_ip, dst_ip, proto, dst_port, in_port)
  - action: "forward:PORT" | "drop" | "flood"
- `SDNSwitch(switch_id)` - OpenFlow-коммутатор с flow table
  - `install_rule(rule)` - устанавливает правило
  - `process_packet(packet)` -> str - обрабатывает пакет, возвращает действие
  - `flow_stats()` -> list - статистика по правилам (hits)
- `SDNController` - управляет коммутаторами
  - `register_switch(switch)` - регистрирует коммутатор
  - `push_policy(switch_id, rules)` - загружает набор правил

## Пример вызова

```python
from solution import SDNSwitch, SDNController, FlowRule

sw = SDNSwitch("sw1")
ctrl = SDNController()
ctrl.register_switch(sw)

rules = [
    FlowRule(priority=100, match={"dst_ip": "10.0.0.1"}, action="forward:1"),
    FlowRule(priority=90,  match={"proto": "icmp"},       action="drop"),
    FlowRule(priority=1,   match={},                      action="flood"),
]
ctrl.push_policy("sw1", rules)

pkts = [
    {"src_ip": "10.0.0.5", "dst_ip": "10.0.0.1", "proto": "tcp", "dst_port": 80},
    {"src_ip": "10.0.0.5", "dst_ip": "10.0.0.2", "proto": "icmp", "dst_port": 0},
    {"src_ip": "10.0.0.5", "dst_ip": "10.0.0.9", "proto": "udp",  "dst_port": 53},
]
for pkt in pkts:
    action = sw.process_packet(pkt)
    print(f"{pkt['dst_ip']} / {pkt['proto']:4s} -> {action}")

print()
for stat in sw.flow_stats():
    print(f"  priority={stat['priority']} hits={stat['hits']} action={stat['action']}")
```

## Ожидаемый вывод

```
10.0.0.1 / tcp  -> forward:1
10.0.0.2 / icmp -> drop
10.0.0.9 / udp  -> flood

  priority=100 hits=1 action=forward:1
  priority=90 hits=1 action=drop
  priority=1 hits=1 action=flood
```

## Запуск

```bash
python3 solution.py
```
