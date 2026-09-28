# Задание 15. Симулятор NAT (Network Address Translation)

## Условие

Класс NATTable симулирует NAPT (PAT): преобразование IP+порт частной сетив общедоступный IP с динамическим портом.
Файл: solution.py Методы
• translate_out(src_ip, src_port, dst_ip, dst_port) -> tuple[str, int]
• возвращает (public_ip, mapped_port); создает запись в таблице
• translate_in(dst_port) -> tuple[str, int] \| None
• обратный перевод по mapped_port → (private_ip, private_port)
• table() -> list[dict]

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import NATTable
nat = NATTable(public_ip="203.0.113.1", port_start=10000)
pub_ip, pub_port = nat.translate_out("192.168.1.10", 54321, "8.8.8.8", 53)
print(pub_ip, pub_port)
priv = nat.translate_in(pub_port)
print(priv)
print(nat.table())
```

## Ожидаемый вывод

```
203.0.113.1 10000
('192.168.1.10', 54321)
[{'priv_ip': '192.168.1.10', 'priv_port': 54321, 'pub_port': 10000, 'dst_ip': '8.8.8.8', 'dst_port': 53}]
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
