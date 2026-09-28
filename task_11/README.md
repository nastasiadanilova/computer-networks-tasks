# Задание 11. Симулятор DNS-резолвера с рекурсией и кешем

## Условие

Класс DNSResolver с кешем записей и рекурсивным разворачиванием CNAME.
Файл: solution.py Методы
• load_zone(zone: dict) - загрузить зону (словарь {имя: {тип: [значения]}})
• resolve(name, rtype="A") -> list \| None - вернуть список значений или None
• cache_stats() -> dict - {"hits": int, "misses": int, "entries": int}Поддерживаемые типы: A, CNAME, MX, TXT

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import DNSResolver
d = DNSResolver()
d.load_zone({
    "www.lab.local": {"A": ["10.0.0.10"]},
    "ftp.lab.local": {"CNAME": ["www.lab.local"]},
    "lab.local":     {"MX": [(10, "mail.lab.local")],
                      "TXT": ["v=spf1 include:lab.local ~all"]},
    "mail.lab.local":{"A": ["10.0.0.20"]},
})
print(d.resolve("ftp.lab.local", "A"))
print(d.resolve("ftp.lab.local", "A"))  # из кеша
print(d.resolve("lab.local", "MX"))
print(d.cache_stats())
```

## Ожидаемый вывод

```
['10.0.0.10']
['10.0.0.10']
[(10, 'mail.lab.local')]
{'hits': 1, 'misses': 2, 'entries': 2}
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
