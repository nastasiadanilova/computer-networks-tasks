# Задание 19. Симулятор VLAN-коммутатора

## Условие

Класс VLANSwitch симулирует работу управляемого коммутатора с поддержкой VLAN.
Файл: solution.py
Методы:
  add_vlan(vlan_id, name)               -- создать VLAN
  set_access(port, vlan_id)              -- назначить порт в access-режим
  set_trunk(port, allowed_vlans)         -- trunk-порт (список VLAN)
  send_frame(src_port, dst_mac, payload) -- вернуть список портов-получателей
  mac_table() -> dict                    -- таблица MAC-адресов {mac: (port, vlan_id)}
Логика: access-порт тегируется при входе; trunk-порт сохраняет тег; flooding при неизвестном dst.

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import VLANSwitch
sw = VLANSwitch()
sw.add_vlan(10, "Sales"); sw.add_vlan(20, "IT")
sw.set_access("fa0/1", 10); sw.set_access("fa0/2", 10); sw.set_access("fa0/3", 20)
# фрейм с fa0/1 (VLAN10), dst неизвестен → flooding в VLAN10
print(sw.send_frame("fa0/1", "ff:ff:ff:ff:ff:ff", "ARP request"))
# фрейм с fa0/3 (VLAN20) → flood только в VLAN20
print(sw.send_frame("fa0/3", "ff:ff:ff:ff:ff:ff", "ARP request"))
```

## Ожидаемый вывод

```
['fa0/2']
[]
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
