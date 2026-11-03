# Задание 36. Симулятор протокола RIP (Distance Vector)

## Условие

Реализовать класс `RIPNetwork`, симулирующий работу протокола RIP (Routing Information Protocol). Маршрутизаторы обмениваются таблицами маршрутизации итеративно до сходимости.
Файл: solution.py

## Класс RIPNetwork

- `__init__()` - создает пустую сеть
- `add_link(r1, r2, cost)` - добавляет двунаправленный линк между маршрутизаторами
- `run(max_iterations=20)` -> int - запускает обмен маршрутами, возвращает число итераций до сходимости
- `table(router)` -> dict - таблица маршрутизации: {"dst": (cost, next_hop)}

## Пример вызова

```python
from solution import RIPNetwork

net = RIPNetwork()
net.add_link("R1", "R2", 1)
net.add_link("R2", "R3", 2)
net.add_link("R1", "R3", 10)

iters = net.run()
print(f"Converged in {iters} iterations")
for dst, (cost, hop) in sorted(net.table("R1").items()):
    print(f"  -> {dst}: cost={cost}, next_hop={hop}")
```

## Ожидаемый вывод

```
Converged in 2 iterations
  -> R1: cost=0, next_hop=R1
  -> R2: cost=1, next_hop=R2
  -> R3: cost=3, next_hop=R2
```

## Запуск

```bash
python3 solution.py
```
