# Задание 32. SMTP-клиент поверх raw-сокета

## Условие

Реализовать класс `SMTPClient`, который отправляет письмо через SMTP-сервер, используя только модуль `socket`. Реализовать диалог EHLO/MAIL FROM/RCPT TO/DATA/QUIT.
Файл: solution.py

## Класс SMTPClient

- `__init__(host, port=25)`
- `send(from_addr, to_addr, subject, body)` -> list[str] - возвращает лог диалога
- `quit()`

## Пример вызова

```python
from solution import SMTPClient

client = SMTPClient("127.0.0.1", port=2525)
log = client.send(
    from_addr="sender@example.com",
    to_addr="recipient@example.com",
    subject="Test",
    body="Hello from raw socket!"
)
for line in log:
    print(line)
```

## Ожидаемый вывод

```
>> EHLO localhost
<< 250-Hello
>> MAIL FROM:<sender@example.com>
<< 250 OK
>> RCPT TO:<recipient@example.com>
<< 250 OK
>> DATA
<< 354 Start input
>> (message body)
<< 250 OK
>> QUIT
<< 221 Bye
```

## Запуск

```bash
python3 solution.py
```
