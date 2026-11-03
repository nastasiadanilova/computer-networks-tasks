# Задание 47. Симулятор распределенной хеш-таблицы (кольцо Chord)

## Условие

Реализовать симулятор кольца Chord (DHT) - распределенной хеш-таблицы из статьи Stoica et al. 2001. Узлы расположены на кольце [0, 2^m), каждый отвечает за диапазон ключей. Реализовать join, lookup и store/get.
Файл: solution.py

## Класс ChordRing

- `__init__(m=8)` - кольцо размером 2^m (m бит)
- `join(node_id)` - добавляет узел в кольцо
- `leave(node_id)` - удаляет узел
- `responsible(key_hash)` -> node_id - узел, ответственный за ключ
- `store(key, value)` - сохраняет значение в ответственном узле
- `get(key)` -> value - получает значение

## Пример вызова

```python
from solution import ChordRing

ring = ChordRing(m=8)
for node in [10, 50, 100, 200]:
    ring.join(node)

print("Nodes:", sorted(ring.nodes))
print("Responsible for key 30:", ring.responsible(30))
print("Responsible for key 75:", ring.responsible(75))

ring.store("hostname", "router-01")
print("get hostname:", ring.get("hostname"))
```

## Ожидаемый вывод

```
Nodes: [10, 50, 100, 200]
Responsible for key 30: 50
Responsible for key 75: 100
get hostname: router-01
```

## Запуск

```bash
python3 solution.py
```
