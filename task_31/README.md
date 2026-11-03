# Задание 31. HTTP/1.1-клиент поверх raw-сокета

## Условие

Реализовать HTTP/1.1-клиент без использования модуля `urllib` или `requests`. Использовать только модуль `socket`. Клиент выполняет GET-запрос и разбирает ответ на статус, заголовки и тело.
Файл: solution.py

## Функции

- `http_get(host, path="/", port=80)` -> dict

Возвращает: `{"status": int, "headers": dict, "body": str}`

## Пример вызова

```python
from solution import http_get

resp = http_get("example.com", "/")
print(resp["status"])
print(resp["headers"].get("content-type", ""))
print(resp["body"][:80])
```

## Ожидаемый вывод

```
200
text/html; charset=UTF-8
<!doctype html>
<html>
<head>
    <title>Example Domain</title>
```

## Запуск

```bash
python3 solution.py
```
