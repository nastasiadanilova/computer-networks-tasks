# Задание 14. Симулятор DHCP-сервера

## Условие

Класс DHCPServer симулирует выдачу IP-адресов клиентам по MAC-адресу.
Файл: solution.py Методы
• __init__(pool_network, lease_time=86400, dns=None, gw=None)
• discover(mac) -> dict - DHCP OFFER (предлагает IP)
• request(mac, requested_ip) -> dict - DHCP ACK/NAK
• release(mac) - освобождает аренду
• leases() -> list[dict] - текущие аренды
• available_count() -> int

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import DHCPServer
srv = DHCPServer("192.168.100.0/28", lease_time=3600,
                 dns="8.8.8.8", gw="192.168.100.1")
offer = srv.discover("aa:bb:cc:dd:ee:01")
print(offer)
ack = srv.request("aa:bb:cc:dd:ee:01", offer["offered_ip"])
print(ack)
print(srv.available_count())
```

## Ожидаемый вывод

```
{'offered_ip': '192.168.100.2', 'lease_time': 3600, 'dns': '8.8.8.8', 'gw': '192.168.100.1'}
{'status': 'ACK', 'ip': '192.168.100.2', 'mac': 'aa:bb:cc:dd:ee:01', 'lease_time': 3600}
12
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
