# Задание 20. Парсер конфигурации Cisco IOS

## Условие

Функция parse_cisco_config(text: str) -> dict парсит текст конфигурации Cisco IOS
и возвращает структурированный словарь.
Файл: solution.py
Поля: hostname, interfaces (ip, mask, description, shutdown),
       static_routes, acls, ntp_server, dns_servers

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import parse_cisco_config
cfg = open("example.cfg").read()
import pprint; pprint.pprint(parse_cisco_config(cfg))
```

## Ожидаемый вывод

```

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
