# Задание 02. Определение класса IPv4-адреса

## Условие

Напишите функцию ip_class(ip: str) -> dict, которая принимает строку IPv4-адреса
и возвращает словарь с информацией о классе адреса.
Формат: {"ip": "192.168.1.1", "class": "C", "type": "private",
         "default_mask": "255.255.255.0", "first_octet": 192}
Типы: private, public, loopback, multicast, reserved.

## Параметры

| | |
|---|---|
| Сигнатура | `ip_class(ip: str) -> dict` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import ip_class
print(ip_class("192.168.1.1"))
print(ip_class("10.0.0.1"))
print(ip_class("8.8.8.8"))
```

## Ожидаемый вывод

```
{'ip': '192.168.1.1', 'class': 'C', 'type': 'private', 'default_mask': '255.255.255.0', 'first_octet': 192}
{'ip': '10.0.0.1', 'class': 'A', 'type': 'private', 'default_mask': '255.0.0.0', 'first_octet': 10}
{'ip': '8.8.8.8', 'class': 'A', 'type': 'public', 'default_mask': '255.0.0.0', 'first_octet': 8}
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
