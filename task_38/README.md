# Задание 38. Симулятор MPLS-коммутации меток

## Условие

Реализовать класс `MPLSRouter`, симулирующий Label Switching Router (LSR). Маршрутизатор хранит таблицу меток (Label Forwarding Information Base, LFIB) и выполняет операции PUSH, SWAP, POP над стеком меток пакета.
Файл: solution.py

## Класс MPLSRouter

- `__init__(name)` - создает маршрутизатор с именем
- `add_lfib_entry(in_label, action, out_label, out_interface)` - добавляет запись в LFIB
  - action: "PUSH" | "SWAP" | "POP"
- `forward(packet)` -> dict - обрабатывает пакет, возвращает измененный пакет с новым стеком меток

Пакет: `{"src": str, "dst": str, "label_stack": list[int], "payload": str}`

## Пример вызова

```python
from solution import MPLSRouter

r1 = MPLSRouter("R1")
r1.add_lfib_entry(in_label=None,   action="PUSH", out_label=100, out_interface="eth1")
r1.add_lfib_entry(in_label=100,    action="SWAP", out_label=200, out_interface="eth2")
r1.add_lfib_entry(in_label=200,    action="POP",  out_label=None, out_interface="eth3")

pkt = {"src": "10.0.0.1", "dst": "10.0.0.2", "label_stack": [], "payload": "data"}
pkt = r1.forward(pkt, in_label=None)
print(pkt["label_stack"], "->", pkt["out_interface"])
pkt = r1.forward(pkt, in_label=100)
print(pkt["label_stack"], "->", pkt["out_interface"])
pkt = r1.forward(pkt, in_label=200)
print(pkt["label_stack"], "->", pkt["out_interface"])
```

## Ожидаемый вывод

```
[100] -> eth1
[200] -> eth2
[] -> eth3
```

## Запуск

```bash
python3 solution.py
```
