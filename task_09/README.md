# Задание 09. Симулятор longest-prefix-match маршрутизации

## Условие

Класс Router с методами:
  add_route(network, next_hop, iface, metric=1)
  remove_route(network)
  lookup(dst_ip) -> dict
  show_table() -> list[dict]
Возвращаемый lookup: {"dst": "8.8.8.8", "matched_route": "0.0.0.0/0",
                      "next_hop": "10.0.0.1", "iface": "eth0", "metric": 1}

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import Router
r = Router()
r.add_route("192.168.1.0/24", None, "eth0")
r.add_route("10.0.0.0/8", "192.168.1.1", "eth1", metric=10)
r.add_route("0.0.0.0/0", "10.0.0.1", "eth0", metric=1)
print(r.lookup("192.168.1.55"))
print(r.lookup("8.8.8.8"))
for row in r.show_table():
    print(row)
```

## Ожидаемый вывод

```
{'dst': '192.168.1.55', 'matched_route': '192.168.1.0/24', 'next_hop': None, 'iface': 'eth0', 'metric': 1}
{'dst': '8.8.8.8', 'matched_route': '0.0.0.0/0', 'next_hop': '10.0.0.1', 'iface': 'eth0', 'metric': 1}
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
