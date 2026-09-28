# Задание 10. HTTP REST API сервер (GET/POST/DELETE)

## Условие

Напишите HTTP-сервер без сторонних фреймворков (только http.server),
поддерживающий простое REST API для управления списком устройств сети.
Файл: server.py
Эндпоинты:
  GET    /devices          -- список всех устройств (200)
  GET    /devices/{id}     -- устройство по ID (200/404)
  POST   /devices          -- создать устройство (201)
  DELETE /devices/{id}     -- удалить устройство (200/404)

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

- • Все ответы - валидный JSON
- • Content-Type: application/json во всех ответах
- • id - автоинкремент начиная с 1

## Запуск

```bash
python3 solution.py
```

Через Docker:
```bash
docker run --rm -v $(pwd):/app python:3.11-slim python3 /app/solution.py
```
