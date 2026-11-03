# Задание 46. Построитель и анализатор TCP-сегмента

## Условие

Реализовать класс `TCPSegment` для построения и разбора TCP-сегментов с вычислением настоящей контрольной суммы (RFC 793 pseudo-header). Поддерживать все поля TCP-заголовка.
Файл: solution.py

## Класс TCPSegment

- `__init__(src_port, dst_port, seq, ack, flags, window, payload=b"")` - конструктор
- `build(src_ip, dst_ip)` -> bytes - сборка сегмента с вычислением checksum
- `TCPSegment.parse(raw_bytes, src_ip, dst_ip)` -> TCPSegment - разбор из байт
- `verify_checksum(src_ip, dst_ip)` -> bool - проверка контрольной суммы

Флаги задаются как строка: "SYN", "ACK", "SYN+ACK", "FIN", "RST", "PSH+ACK"

## Пример вызова

```python
from solution import TCPSegment

seg = TCPSegment(
    src_port=12345, dst_port=80,
    seq=1000, ack=0,
    flags="SYN", window=65535,
    payload=b""
)
raw = seg.build("192.168.1.1", "192.168.1.2")
print(f"Built {len(raw)} bytes")

parsed = TCPSegment.parse(raw, "192.168.1.1", "192.168.1.2")
print(f"src_port={parsed.src_port}, dst_port={parsed.dst_port}")
print(f"seq={parsed.seq}, flags={parsed.flags}")
print(f"checksum valid: {parsed.verify_checksum('192.168.1.1', '192.168.1.2')}")
```

## Ожидаемый вывод

```
Built 20 bytes
src_port=12345, dst_port=80
seq=1000, flags=SYN
checksum valid: True
```

## Запуск

```bash
python3 solution.py
```
