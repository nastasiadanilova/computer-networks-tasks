# Задание 33. Разбор заголовков Ethernet/IP/TCP из hex-дампа

## Условие

Реализовать функцию `parse_packet(hex_str)`, которая принимает hex-строку сетевого пакета и возвращает словарь с разобранными полями Ethernet, IP и TCP заголовков.
Файл: solution.py

## Функции

- `parse_packet(hex_str)` -> dict с полями: `ethernet`, `ip`, `tcp` (или `udp`, или `payload`)

## Пример вызова

```python
from solution import parse_packet

# Ethernet + IP + TCP SYN пакет (минимальный, без данных)
hex_pkt = (
    "ffffffffffff"   # dst MAC: broadcast
    "aabbccddeeff"   # src MAC
    "0800"           # EtherType: IPv4
    "45000028"       # IP: ver=4, IHL=5, TOS=0, len=40
    "12340000"       # ID, flags/frag
    "4006"           # TTL=64, proto=6 (TCP)
    "0000"           # checksum (0 for demo)
    "c0a80101"       # src IP: 192.168.1.1
    "c0a80102"       # dst IP: 192.168.1.2
    "1f90"           # src port: 8080
    "0050"           # dst port: 80
    "00000001"       # seq=1
    "00000000"       # ack=0
    "5002"           # offset=5, flags=SYN
    "ffff"           # window
    "0000"           # checksum
    "0000"           # urgent
)
result = parse_packet(hex_pkt)
print(result["ethernet"])
print(result["ip"])
print(result["tcp"])
```

## Ожидаемый вывод

```
{'dst': 'ff:ff:ff:ff:ff:ff', 'src': 'aa:bb:cc:dd:ee:ff', 'ethertype': '0x0800'}
{'version': 4, 'ihl': 5, 'ttl': 64, 'proto': 6, 'src': '192.168.1.1', 'dst': '192.168.1.2', 'length': 40}
{'src_port': 8080, 'dst_port': 80, 'seq': 1, 'ack': 0, 'flags': 'SYN', 'window': 65535}
```

## Запуск

```bash
python3 solution.py
```
