"""
Задание 46. Построитель и анализатор TCP-сегмента.

Полная реализация TCP-заголовка с вычислением checksum через pseudo-header (RFC 793).
"""

import struct
import socket


# Битовые маски TCP-флагов
_FLAG_MAP = {
    "FIN": 0x001,
    "SYN": 0x002,
    "RST": 0x004,
    "PSH": 0x008,
    "ACK": 0x010,
    "URG": 0x020,
}


def _flags_to_int(flags_str: str) -> int:
    """Преобразует строку "SYN+ACK" в числовое значение."""
    result = 0
    for part in flags_str.upper().split("+"):
        part = part.strip()
        if part in _FLAG_MAP:
            result |= _FLAG_MAP[part]
    return result


def _int_to_flags(flags_int: int) -> str:
    """Преобразует числовое значение флагов в строку "SYN+ACK"."""
    active = [name for name, bit in _FLAG_MAP.items() if flags_int & bit]
    return "+".join(active) if active else "NONE"


def _inet_aton(ip: str) -> bytes:
    return socket.inet_aton(ip)


def _checksum(data: bytes) -> int:
    """Вычисляет 16-битную контрольную сумму RFC 1071."""
    if len(data) % 2:
        data += b"\x00"
    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF


def _pseudo_header(src_ip: str, dst_ip: str, tcp_len: int) -> bytes:
    """Строит псевдо-заголовок для вычисления контрольной суммы TCP."""
    return (
        _inet_aton(src_ip) +
        _inet_aton(dst_ip) +
        struct.pack("!BBH", 0, 6, tcp_len)  # reserved, proto=TCP, length
    )


class TCPSegment:
    """
    TCP-сегмент с полным набором полей заголовка.

    Поддерживает сборку в байты и разбор из байт с верификацией checksum.
    """

    def __init__(
        self,
        src_port: int,
        dst_port: int,
        seq: int,
        ack: int,
        flags: str,
        window: int,
        payload: bytes = b"",
        urgent: int = 0,
    ):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq = seq
        self.ack = ack
        self.flags = flags.upper()
        self.window = window
        self.payload = payload
        self.urgent = urgent
        self._raw_checksum: int = 0  # заполняется при разборе

    def build(self, src_ip: str, dst_ip: str) -> bytes:
        """
        Собирает TCP-сегмент в байты с вычисленным checksum.

        Args:
            src_ip: IP-адрес источника (для pseudo-header)
            dst_ip: IP-адрес назначения (для pseudo-header)

        Returns:
            Байты TCP-сегмента (заголовок + данные).
        """
        flags_int = _flags_to_int(self.flags)
        data_offset = 5  # 5 * 4 = 20 байт (без опций)
        # data_offset занимает верхние 4 бита; нижние 12 - зарезервированы + флаги
        offset_flags = (data_offset << 12) | flags_int

        # Заголовок с нулевым checksum для вычисления
        header = struct.pack(
            "!HHIIHHHH",
            self.src_port,
            self.dst_port,
            self.seq,
            self.ack,
            offset_flags,
            self.window,
            0,
            self.urgent,
        )

        segment = header + self.payload
        pseudo = _pseudo_header(src_ip, dst_ip, len(segment))
        csum = _checksum(pseudo + segment)

        # Вставляем вычисленный checksum (смещение 16 байт от начала заголовка)
        segment = segment[:16] + struct.pack("!H", csum) + segment[18:]
        self._raw_checksum = csum
        return segment

    @classmethod
    def parse(cls, raw: bytes, src_ip: str, dst_ip: str) -> "TCPSegment":
        """
        Разбирает байты TCP-сегмента.

        Args:
            raw: байты сегмента (только TCP, без IP-заголовка)
            src_ip: IP источника (из IP-заголовка) для хранения
            dst_ip: IP назначения

        Returns:
            Экземпляр TCPSegment с заполненными полями.
        """
        src_port, dst_port, seq, ack, offset_flags, window, checksum, urgent = \
            struct.unpack("!HHIIHHHH", raw[:20])

        data_offset = (offset_flags >> 12) * 4
        flags_int = offset_flags & 0x01FF
        payload = raw[data_offset:]

        seg = cls(
            src_port=src_port,
            dst_port=dst_port,
            seq=seq,
            ack=ack,
            flags=_int_to_flags(flags_int),
            window=window,
            payload=payload,
            urgent=urgent,
        )
        seg._raw_checksum = checksum
        seg._src_ip = src_ip
        seg._dst_ip = dst_ip
        seg._raw = raw
        return seg

    def verify_checksum(self, src_ip: str, dst_ip: str) -> bool:
        """Проверяет контрольную сумму разобранного сегмента."""
        if not hasattr(self, "_raw"):
            return False
        pseudo = _pseudo_header(src_ip, dst_ip, len(self._raw))
        return _checksum(pseudo + self._raw) == 0


if __name__ == "__main__":
    seg = TCPSegment(
        src_port=12345, dst_port=80,
        seq=1000, ack=0,
        flags="SYN", window=65535,
        payload=b"",
    )
    raw = seg.build("192.168.1.1", "192.168.1.2")
    print(f"Built {len(raw)} bytes")

    parsed = TCPSegment.parse(raw, "192.168.1.1", "192.168.1.2")
    print(f"src_port={parsed.src_port}, dst_port={parsed.dst_port}")
    print(f"seq={parsed.seq}, flags={parsed.flags}")
    print(f"checksum valid: {parsed.verify_checksum('192.168.1.1', '192.168.1.2')}")
