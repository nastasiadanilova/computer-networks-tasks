# Задание 39. Симулятор SNMP MIB

## Условие

Реализовать класс `SNMPAgent`, симулирующий SNMP-агент с деревом MIB. Поддерживать операции GET, SET, GETNEXT (обход дерева OID).
Файл: solution.py

## Класс SNMPAgent

- `__init__()` - создает агент с базовыми OID (sysDescr, sysUpTime, sysName)
- `register(oid, value, writable=False)` - регистрирует OID в MIB
- `get(oid)` -> value - возвращает значение OID
- `set(oid, value)` -> bool - устанавливает значение (если writable)
- `getnext(oid)` -> (next_oid, value) - следующий OID в лексикографическом порядке
- `walk(start_oid)` -> list[(oid, value)] - обход поддерева

## Пример вызова

```python
from solution import SNMPAgent

agent = SNMPAgent()
agent.register("1.3.6.1.2.1.1.1.0", "Linux Router 2.6", writable=False)
agent.register("1.3.6.1.2.1.1.5.0", "router01",         writable=True)
agent.register("1.3.6.1.2.1.2.1.0", 3,                  writable=False)

print(agent.get("1.3.6.1.2.1.1.1.0"))
agent.set("1.3.6.1.2.1.1.5.0", "core-router")
print(agent.get("1.3.6.1.2.1.1.5.0"))

for oid, val in agent.walk("1.3.6.1.2.1.1"):
    print(f"  {oid} = {val}")
```

## Ожидаемый вывод

```
Linux Router 2.6
core-router
  1.3.6.1.2.1.1.1.0 = Linux Router 2.6
  1.3.6.1.2.1.1.5.0 = core-router
```

## Запуск

```bash
python3 solution.py
```
