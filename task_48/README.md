# Задание 48. Симулятор протокола AODV (реактивная маршрутизация)

## Условие

Реализовать симулятор протокола AODV (Ad hoc On-Demand Distance Vector). Узлы рассылают RREQ (Route Request) при необходимости маршрута и получают RREP (Route Reply) обратно. Поддерживать таблицу маршрутов и последовательные номера (sequence numbers).
Файл: solution.py

## Класс AODVNode и AODVNetwork

- `AODVNetwork` - управляет топологией и доставкой сообщений
- `AODVNetwork.add_link(n1, n2)` - добавляет линк (беспроводное соединение)
- `AODVNetwork.route_discovery(src, dst)` -> list[str] - запускает RREQ, возвращает найденный путь
- `AODVNetwork.routing_table(node)` -> dict - таблица маршрутов узла

## Пример вызова

```python
from solution import AODVNetwork

net = AODVNetwork()
net.add_link("A", "B")
net.add_link("B", "C")
net.add_link("C", "D")
net.add_link("A", "C")  # прямой путь A->C

path = net.route_discovery("A", "D")
print("Path A->D:", path)

path2 = net.route_discovery("A", "C")
print("Path A->C:", path2)

print("A routing table:", net.routing_table("A"))
```

## Ожидаемый вывод

```
Path A->D: ['A', 'C', 'D']
Path A->C: ['A', 'C']
A routing table: {'D': {'next_hop': 'C', 'hops': 2}, 'C': {'next_hop': 'C', 'hops': 1}}
```

## Запуск

```bash
python3 solution.py
```
