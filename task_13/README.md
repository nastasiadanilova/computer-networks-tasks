# Задание 13. Симулятор ACL (расширенный с логированием)

## Условие

Класс ACL с методами загрузки правил, проверки пакета и просмотра лога.
Файл: solution.py Методы
• add_rule(action, proto, src, dst, dst_port=None, description="")
• check(packet: dict) -> dict - возвращает {action, rule_index, description}
• log() -> list[dict] - история всех проверенных пакетов

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
from solution import ACL
acl = ACL()
acl.add_rule("permit","tcp","203.0.113.5/32","192.168.1.100/32",22,"admin SSH")
acl.add_rule("deny",  "tcp","any",           "192.168.1.100/32",22,"block SSH")
acl.add_rule("permit","any","192.168.1.0/24","any",None,          "LAN out")

pkt1 = {"proto":"tcp","src":"203.0.113.5","dst":"192.168.1.100","dst_port":22}
pkt2 = {"proto":"tcp","src":"1.2.3.4",    "dst":"192.168.1.100","dst_port":22}
pkt3 = {"proto":"udp","src":"192.168.1.5","dst":"8.8.8.8",      "dst_port":53}
pkt4 = {"proto":"tcp","src":"5.5.5.5",    "dst":"8.8.8.8",      "dst_port":80}
for p in [pkt1,pkt2,pkt3,pkt4]:
    print(acl.check(p))
```

## Ожидаемый вывод

```
{'action': 'permit', 'rule_index': 0, 'description': 'admin SSH'}
{'action': 'deny',   'rule_index': 1, 'description': 'block SSH'}
{'action': 'permit', 'rule_index': 2, 'description': 'LAN out'}
{'action': 'deny',   'rule_index': -1, 'description': 'implicit deny'}
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
