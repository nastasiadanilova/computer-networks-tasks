# Задание 17. TCP-прокси (порт-форвардер)

## Условие

Напишите однонаправленный TCP-прокси: принимает подключения на локальном порту, проксирует трафик к целевому серверу, логирует объем переданных байт.
Файл: proxy.py Запускpython3 proxy.py <local_port> <target_host> <target_port># пример:python3 proxy.py 8888 127.0.0.1 8080 Поведение
• Для каждого входящего соединения открывает соединение к target
• Запускает 2 потока: client→target и target→client
• Логирует: [proxy] client→target: N bytes, [proxy] target→client: N bytes
• Graceful shutdown по Ctrl+CТестpython3 -m http.server 8080 &python3 proxy.py 8888 127.0.0.1 8080 &

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python

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
