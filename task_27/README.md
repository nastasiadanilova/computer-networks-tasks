# Задание 27. Многопоточный HTTP-загрузчик с повторными попытками

## Условие

download_all(urls: list[str], workers=4, retries=3, timeout=5) -> list[dict]
Параллельно скачивает URL-адреса, при ошибке повторяет до retries раз.
Файл: solution.py
Элемент ответа: {"url": "http://...", "status": 200, "bytes": 1234, "attempts": 1, "error": None}
При неудаче: {"url":..., "status": None, "bytes": 0, "attempts": 3, "error": "timeout"}

## Параметры

| | |
|---|---|
| Сигнатура | `` |
| Входные данные |  |
| Выходные данные |  |

## Пример вызова

```python
python3 solution.py http://httpbin.org/get http://httpbin.org/status/404
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
