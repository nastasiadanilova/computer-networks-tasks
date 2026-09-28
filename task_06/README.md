# Задание 06. UDP-чат (клиент-сервер)

## Условие

Напишите UDP-сервер, который принимает датаграммы от клиентов и ретранслирует
их всем остальным (broadcast-over-UDP через список клиентов).
Файлы: server.py, client.py
server.py:
  - Слушает 127.0.0.1:9191 (UDP)
  - Поддерживает dict активных клиентов (addr -> nickname)
  - Протокол: первое сообщение JOIN:<nickname>, далее MSG:<text>, выход - LEAVE
  - При получении MSG ретранслирует всем КРОМЕ отправителя: <nickname>: <text>
client.py:
  - Аргументы: nickname, [message]
  - Отправляет JOIN, затем сообщение, затем LEAVE

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
python3 server.py &
python3 client.py Alice "Hello everyone"
```

## Ожидаемый вывод

```
[server] Alice joined
[server] Alice: Hello everyone -> broadcast to 0 peers
[server] Alice left
```

## Критерии приемки

- Сервер не падает при потере пакета (UDP -- no guarantee)
- Timeout на recv в клиенте (3 сек), чтобы не зависал

## Запуск

```bash
python3 solution.py
```

Через Docker:
```bash
docker run --rm -v $(pwd):/app python:3.11-slim python3 /app/solution.py
```
