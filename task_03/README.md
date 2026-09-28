# Задание 03. Калькулятор подсетей FLSM

## Условие

Функция subnet_calc(network: str, new_prefix: int) -> list[dict]
делит сеть на равные подсети и возвращает полную информацию о каждой.
Структура элемента:
{"index": 0, "network": "192.168.1.0/26", "netmask": "255.255.255.192",
 "wildcard": "0.0.0.63", "first_host": "192.168.1.1",
 "last_host": "192.168.1.62", "broadcast": "192.168.1.63",
 "total_hosts": 64, "usable_hosts": 62}

## Параметры

| | |
|---|---|
| Сигнатура | `subnet_calc(network: str, new_prefix: int) -> list[dict]` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import subnet_calc
for s in subnet_calc("192.168.1.0/24", 26):
    print(s)
```

## Ожидаемый вывод

```
{'index': 0, 'network': '192.168.1.0/26', ...}
... (итого 4 подсети)
```

## Критерии приемки

- Ключи словаря строго как указано
- wildcard = инверсия маски
- ValueError если new_prefix <= исходный или new_prefix > 30

## Запуск

```bash
python3 solution.py
```

Через Docker:
```bash
docker run --rm -v $(pwd):/app python:3.11-slim python3 /app/solution.py
```
