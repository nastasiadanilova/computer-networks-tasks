"""
Задание 33. Разбор заголовков Ethernet/IP/TCP из hex-дампа.

Парсит бинарный пакет (в виде hex-строки) по полям протоколов.
"""

import struct


# Отображение номеров протоколов IP в имена
_IP_PROTO = {1: "ICMP", 6: "TCP", 17: "UDP", 89: "OSPF"}

# Биты TCP-флагов
_TCP_FLAGS = {
    0x001: "FIN",
    0x002: "SYN",
    0x004: "RST",
    0x008: "PSH",
    0x010: "ACK",
    0x020: "URG",
}


def _mac_str(raw: bytes) -> str:
    return ":".join(f"{b:02x}" for b in raw)


def _ip_str(raw: bytes) -> str:
    return ".".join(str(b) for b in raw)


def _tcp_flag_names(flags: int) -> str:
    active = [name for bit, name in _TCP_FLAGS.items() if flags & bit]
    return "+".join(active) if active else "NONE"


def parse_packet(hex_str: str) -> dict:
    """
    Разбирает hex-строку сетевого пакета.

    Поддерживает стек Ethernet II -> IPv4 -> TCP/UDP.
    Возвращает словарь с ключами 'ethernet', 'ip', и 'tcp'/'udp'/'payload'.
    """
    raw = bytes.fromhex(hex_str.replace(" ", "").replace("\n", ""))
    offset = 0

    # ── Ethernet II (14 байт) ─────────────────────────────────────────────
    dst_mac = raw[offset:offset + 6]
    src_mac = raw[offset + 6:offset + 12]
    ethertype = struct.unpack("!H", raw[offset + 12:offset + 14])[0]
    offset += 14

    ethernet = {
        "dst": _mac_str(dst_mac),
        "src": _mac_str(src_mac),
        "ethertype": f"0x{ethertype:04x}",
    }

    result: dict = {"ethernet": ethernet}

    if ethertype != 0x0800:
        result["payload"] = raw[offset:].hex()
        return result

    # ── IPv4 ──────────────────────────────────────────────────────────────
    ip_start = offset
    ver_ihl = raw[offset]
    version = ver_ihl >> 4
    ihl = ver_ihl & 0x0F          # в 32-битных словах
    tos = raw[offset + 1]
    total_len = struct.unpack("!H", raw[offset + 2:offset + 4])[0]
    ttl = raw[offset + 8]
    proto = raw[offset + 9]
    src_ip = raw[offset + 12:offset + 16]
    dst_ip = raw[offset + 16:offset + 20]
    offset = ip_start + ihl * 4

    ip = {
        "version": version,
        "ihl": ihl,
        "ttl": ttl,
        "proto": proto,
        "src": _ip_str(src_ip),
        "dst": _ip_str(dst_ip),
        "length": total_len,
    }
    result["ip"] = ip

    # ── TCP ───────────────────────────────────────────────────────────────
    if proto == 6 and len(raw) >= offset + 20:
        src_port, dst_port = struct.unpack("!HH", raw[offset:offset + 4])
        seq = struct.unpack("!I", raw[offset + 4:offset + 8])[0]
        ack = struct.unpack("!I", raw[offset + 8:offset + 12])[0]
        data_off_flags = struct.unpack("!H", raw[offset + 12:offset + 14])[0]
        flags = data_off_flags & 0x01FF
        window = struct.unpack("!H", raw[offset + 14:offset + 16])[0]
        result["tcp"] = {
            "src_port": src_port,
            "dst_port": dst_port,
            "seq": seq,
            "ack": ack,
            "flags": _tcp_flag_names(flags),
            "window": window,
        }

    # ── UDP ───────────────────────────────────────────────────────────────
    elif proto == 17 and len(raw) >= offset + 8:
        src_port, dst_port, length, checksum = struct.unpack("!HHHH", raw[offset:offset + 8])
        result["udp"] = {
            "src_port": src_port,
            "dst_port": dst_port,
            "length": length,
        }

    else:
        result["payload"] = raw[offset:].hex()

    return result


if __name__ == "__main__":
    hex_pkt = (
        "ffffffffffff"
        "aabbccddeeff"
        "0800"
        "45000028"
        "12340000"
        "4006"
        "0000"
        "c0a80101"
        "c0a80102"
        "1f90"
        "0050"
        "00000001"
        "00000000"
        "5002"
        "ffff"
        "0000"
        "0000"
    )
    result = parse_packet(hex_pkt)
    print(result["ethernet"])
    print(result["ip"])
    print(result["tcp"])
