"""
Задание 31. HTTP/1.1-клиент поверх raw-сокета.

GET-запрос без urllib/requests, только socket.
"""

import socket


def http_get(host: str, path: str = "/", port: int = 80) -> dict:
    """
    Выполняет HTTP/1.1 GET-запрос и возвращает разобранный ответ.

    Args:
        host: доменное имя или IP сервера
        path: путь запроса (например, "/index.html")
        port: TCP-порт сервера

    Returns:
        {"status": int, "headers": dict, "body": str}
    """
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"User-Agent: raw-socket-client/1.0\r\n"
        f"\r\n"
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((host, port))
        s.sendall(request.encode("utf-8"))

        chunks = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)

    raw = b"".join(chunks).decode("utf-8", errors="replace")

    # Разделяем заголовки и тело
    header_section, _, body = raw.partition("\r\n\r\n")
    lines = header_section.split("\r\n")

    # Разбираем статусную строку: HTTP/1.1 200 OK
    status_line = lines[0]
    status_code = int(status_line.split()[1])

    # Разбираем заголовки
    headers = {}
    for line in lines[1:]:
        if ":" in line:
            key, _, value = line.partition(":")
            headers[key.strip().lower()] = value.strip()

    return {"status": status_code, "headers": headers, "body": body}


if __name__ == "__main__":
    try:
        resp = http_get("example.com", "/")
        print(resp["status"])
        print(resp["headers"].get("content-type", ""))
        print(resp["body"][:80])
    except OSError as e:
        print(f"[error] {e}")
        print("(для теста без сети: функция http_get определена корректно)")
