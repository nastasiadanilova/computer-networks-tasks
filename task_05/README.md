# Задание 05. TCP echo-сервер и клиент

## Условие

Напишите два скрипта: TCP-сервер и TCP-клиент.
Файлы: server.py, client.py
server.py:
  - Слушает 127.0.0.1:9090
  - Принимает строку от клиента, возвращает её в ВЕРХНЕМ РЕГИСТРЕ
  - Логирует: [server] connected: <addr>, [server] recv: <data>, [server] sent: <data>
  - Принимает несколько сообщений в одном соединении (цикл до пустых данных)
client.py:
  - Аргумент командной строки: строка-сообщение
  - Выводит: [client] sent: <msg>, [client] got: <RESPONSE>

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
python3 server.py &
python3 client.py "hello network"
```

## Ожидаемый вывод

```
[client] sent: hello network
[client] got: HELLO NETWORK

[server] connected: ('127.0.0.1', 54321)
[server] recv: hello network
[server] sent: HELLO NETWORK
```

## Критерии приемки

- SO_REUSEADDR установлен
- При пустых данных сервер корректно закрывает соединение
- Ответ всегда в верхнем регистре

## Запуск

```bash
python3 solution.py
```

Через Docker:
```bash
docker run --rm -v $(pwd):/app python:3.11-slim python3 /app/solution.py
```
