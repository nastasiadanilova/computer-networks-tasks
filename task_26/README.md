# Задание 26. Генератор и валидатор MAC-адресов

## Условие

Модуль с набором функций для работы с MAC-адресами.
Файл: solution.py Функции
• is_valid_mac(mac: str) -> bool - проверяет валидность MAC в форматах XX:XX:XX:XX:XX:XX, XX-XX-XX-XX-XX-XX, XXXXXXXXXXXX
• normalize_mac(mac: str) -> str - приводит к формату AA:BB:CC:DD:EE:FF (верхний регистр, двоеточия)
• mac_to_int(mac: str) -> int - MAC → целое число
• int_to_mac(n: int) -> str - целое → MAC
• is_multicast(mac: str) -> bool - бит I/G (первый октет, бит 0)
• is_locally_administered(mac: str) -> bool - бит U/L (первый октет, бит 1)
• oui(mac: str) -> str - первые 3 октета (OUI)
• generate_random_mac(locally_administered=True) -> str

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import *
print(is_valid_mac("aa:bb:cc:dd:ee:ff"))   # True
print(is_valid_mac("ZZ:ZZ:ZZ:ZZ:ZZ:ZZ"))  # False
print(normalize_mac("aa-bb-cc-dd-ee-ff"))  # AA:BB:CC:DD:EE:FF
print(mac_to_int("00:00:00:00:00:01"))     # 1
print(int_to_mac(1))                       # 00:00:00:00:00:01
print(is_multicast("01:00:5e:00:00:01"))   # True
print(oui("AA:BB:CC:DD:EE:FF"))            # AA:BB:CC
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
