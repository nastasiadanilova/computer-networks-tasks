"""
Задание 32. SMTP-клиент поверх raw-сокета.

Реализует диалог EHLO/MAIL FROM/RCPT TO/DATA/QUIT без smtplib.
"""

import socket
import datetime


class SMTPClient:
    """
    Простой SMTP-клиент на чистых сокетах.
    Поддерживает отправку текстового письма через незашифрованное соединение.
    """

    def __init__(self, host: str, port: int = 25):
        self.host = host
        self.port = port
        self._sock = None
        self._log: list = []

    # ── Низкоуровневые методы ────────────────────────────────────────────────

    def _connect(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(10)
        self._sock.connect((self.host, self.port))
        greeting = self._readline()
        self._log.append(f"<< {greeting}")

    def _readline(self) -> str:
        buf = b""
        while not buf.endswith(b"\n"):
            ch = self._sock.recv(1)
            if not ch:
                break
            buf += ch
        return buf.decode("utf-8", errors="replace").strip()

    def _send_cmd(self, cmd: str) -> str:
        self._log.append(f">> {cmd}")
        self._sock.sendall((cmd + "\r\n").encode("utf-8"))
        # Читаем многострочный ответ (250- значит продолжение)
        lines = []
        while True:
            line = self._readline()
            lines.append(line)
            if len(line) < 4 or line[3] != "-":
                break
        response = lines[-1]
        self._log.append(f"<< {response}")
        return response

    # ── Публичный интерфейс ──────────────────────────────────────────────────

    def send(
        self,
        from_addr: str,
        to_addr: str,
        subject: str,
        body: str,
    ) -> list:
        """
        Выполняет SMTP-диалог и отправляет письмо.

        Returns:
            Лог диалога (список строк вида ">> CMD" или "<< RESPONSE")
        """
        self._log.clear()
        self._connect()

        self._send_cmd("EHLO localhost")
        self._send_cmd(f"MAIL FROM:<{from_addr}>")
        self._send_cmd(f"RCPT TO:<{to_addr}>")
        self._send_cmd("DATA")

        date_str = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
        message = (
            f"Date: {date_str}\r\n"
            f"From: {from_addr}\r\n"
            f"To: {to_addr}\r\n"
            f"Subject: {subject}\r\n"
            f"\r\n"
            f"{body}\r\n"
            f".\r\n"
        )
        self._log.append(">> (message body)")
        self._sock.sendall(message.encode("utf-8"))
        resp = self._readline()
        self._log.append(f"<< {resp}")

        self.quit()
        return self._log

    def quit(self):
        """Завершает SMTP-сессию."""
        if self._sock:
            try:
                self._send_cmd("QUIT")
            finally:
                self._sock.close()
                self._sock = None


# ── Демонстрация (без реального SMTP-сервера) ────────────────────────────────

class _MockSMTPServer:
    """Минималистичный mock-сервер SMTP для демонстрации без внешних зависимостей."""

    def __init__(self):
        import threading
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("127.0.0.1", 0))
        self.port = self.server.getsockname()[1]
        self.server.listen(1)
        t = threading.Thread(target=self._handle, daemon=True)
        t.start()

    def _handle(self):
        conn, _ = self.server.accept()
        conn.sendall(b"220 mock SMTP ready\r\n")
        responses = {
            "EHLO": b"250-Hello\r\n250 OK\r\n",
            "MAIL": b"250 OK\r\n",
            "RCPT": b"250 OK\r\n",
            "DATA": b"354 Start input\r\n",
            "QUIT": b"221 Bye\r\n",
        }
        in_data = False
        while True:
            line = b""
            while not line.endswith(b"\n"):
                ch = conn.recv(1)
                if not ch:
                    conn.close()
                    return
                line += ch
            cmd = line.decode().strip()
            if in_data:
                if cmd == ".":
                    conn.sendall(b"250 OK\r\n")
                    in_data = False
                # все остальные строки тела письма игнорируем
                continue
            key = cmd[:4].upper()
            conn.sendall(responses.get(key, b"500 Unknown\r\n"))
            if key == "DATA":
                in_data = True
            if key == "QUIT":
                conn.close()
                return


if __name__ == "__main__":
    srv = _MockSMTPServer()
    client = SMTPClient("127.0.0.1", port=srv.port)
    log = client.send(
        from_addr="sender@example.com",
        to_addr="recipient@example.com",
        subject="Test",
        body="Hello from raw socket!",
    )
    for line in log:
        print(line)
