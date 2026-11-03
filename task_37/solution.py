"""
Задание 37. Симулятор TLS-рукопожатия.

Упрощенная симуляция TLS 1.3 handshake с ECDHE-подобным обменом ключами.
Использует DH на простых числах для демонстрации принципа.
"""

import hashlib
import hmac
import secrets


# Параметры Диффи-Хеллмана (небольшие числа для демонстрации)
# В реальном TLS используется кривая X25519 или P-256
_DH_P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74  # MODP-1024
_DH_G = 2


class TLSHandshake:
    """
    Симулятор TLS 1.3 handshake (учебный, без реального шифрования).

    Демонстрирует порядок сообщений и принцип обмена ключами DH.
    """

    CIPHER_SUITES = [
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
    ]

    def __init__(self, role: str = "client"):
        self.role = role
        self._private_key = secrets.randbelow(_DH_P - 2) + 2
        self._public_key = pow(_DH_G, self._private_key, _DH_P)
        self._random = secrets.token_hex(32)

    def client_hello(self) -> dict:
        """Создает сообщение ClientHello."""
        return {
            "type": "ClientHello",
            "version": "TLS 1.3",
            "random": self._random,
            "cipher_suites": list(self.CIPHER_SUITES),
            "client_public_key": hex(self._public_key),
        }

    def server_hello(self, client_hello: dict) -> dict:
        """
        Создает сообщение ServerHello на основе ClientHello.
        Выбирает первый поддерживаемый шифр.
        """
        chosen = client_hello["cipher_suites"][0]
        return {
            "type": "ServerHello",
            "version": "TLS 1.3",
            "random": self._random,
            "cipher_suite": chosen,
            "server_public_key": hex(self._public_key),
            "client_random": client_hello["random"],
        }

    def derive_keys(self, server_hello: dict) -> dict:
        """
        Клиент вычисляет сессионные ключи из обмена DH.

        Returns:
            {"session_key": hex_str, "iv": hex_str, "cipher_suite": str}
        """
        server_pub = int(server_hello["server_public_key"], 16)
        # Общий секрет DH: (server_pub ^ client_priv) mod P
        shared_secret = pow(server_pub, self._private_key, _DH_P)

        # HKDF-подобное выведение ключей (упрощено до SHA-384)
        shared_bytes = shared_secret.to_bytes(128, "big")
        client_rand = bytes.fromhex(self._random)
        server_rand = bytes.fromhex(server_hello["random"])

        master = hashlib.sha384(shared_bytes + client_rand + server_rand).digest()
        session_key = hashlib.sha384(b"key" + master).hexdigest()
        iv = hashlib.sha256(b"iv" + master).hexdigest()[:24]

        return {
            "session_key": session_key,
            "iv": iv,
            "cipher_suite": server_hello["cipher_suite"],
        }

    def finished(self, keys: dict) -> str:
        """
        Вычисляет Finished MAC для подтверждения завершения handshake.

        Returns:
            HMAC-SHA384 в виде hex-строки.
        """
        key_bytes = bytes.fromhex(keys["session_key"])[:48]
        label = f"finished:{keys['cipher_suite']}:{self.role}".encode()
        mac = hmac.new(key_bytes, label, hashlib.sha384).hexdigest()
        return mac


if __name__ == "__main__":
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
