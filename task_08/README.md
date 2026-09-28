# Задание 08. Симулятор таблицы ARP

## Условие

Напишите класс ARPTable, симулирующий ARP-таблицу коммутатора/хоста:
• хранит пары IP → MAC с TTL (по умолчанию 300 сек)
• методы: add(ip, mac), lookup(ip) -> str\|None, expire(), dump() -> list[dict]

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import ARPTable
import time
arp = ARPTable(ttl=2)
arp.add("192.168.1.1", "aa:bb:cc:dd:ee:ff")
print(arp.lookup("192.168.1.1"))   # aa:bb:cc:dd:ee:ff
time.sleep(3)
arp.expire()
print(arp.lookup("192.168.1.1"))   # None
print(arp.dump())                  # []
```

## Ожидаемый вывод

```
aa:bb:cc:dd:ee:ff
None
[]
```

## Критерии приемки

- MAC-адрес нормализуется к нижнему регистру при добавлении
- expire() удаляет только просроченные записи
- dump() возвращает [{"ip":..., "mac":..., "ttl_left": <float>}]

## Запуск

```bash
python3 solution.py
```

Через Docker:
```bash
docker run --rm -v $(pwd):/app python:3.11-slim python3 /app/solution.py
```
