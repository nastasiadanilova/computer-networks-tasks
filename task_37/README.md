# Задание 37. Симулятор TLS-рукопожатия

## Условие

Реализовать класс `TLSHandshake`, симулирующий упрощенный процесс TLS 1.3 handshake: ClientHello, ServerHello, обмен ключами (ECDHE-подобный), Finished. Использовать стандартные модули Python (hashlib, secrets, hmac).
Файл: solution.py

## Класс TLSHandshake

- `client_hello()` -> dict - генерирует ClientHello с random и поддерживаемыми шифрами
- `server_hello(client_hello)` -> dict - возвращает ServerHello и серверный публичный ключ
- `derive_keys(server_hello)` -> dict - клиент вычисляет сессионные ключи
- `finished(keys)` -> str - вычисляет Finished MAC

## Пример вызова

```python
from solution import TLSHandshake

client = TLSHandshake(role="client")
server = TLSHandshake(role="server")

ch = client.client_hello()
print("ClientHello ciphers:", ch["cipher_suites"])

sh = server.server_hello(ch)
print("ServerHello cipher:", sh["cipher_suite"])

keys = client.derive_keys(sh)
print("Session key (hex):", keys["session_key"][:16], "...")

fin = client.finished(keys)
print("Finished MAC:", fin[:16], "...")
```

## Ожидаемый вывод

```
ClientHello ciphers: ['TLS_AES_256_GCM_SHA384', 'TLS_CHACHA20_POLY1305_SHA256']
ServerHello cipher: TLS_AES_256_GCM_SHA384
Session key (hex): a3f1... ...
Finished MAC: 7d2e... ...
```

(конкретные значения hex меняются при каждом запуске)

## Запуск

```bash
python3 solution.py
```
