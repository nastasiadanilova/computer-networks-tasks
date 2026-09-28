import re, random

def _parse(mac: str) -> list:
    mac = mac.strip().upper().replace("-", ":").replace(".", ":")
    if len(mac) == 12:
        mac = ":".join(mac[i:i+2] for i in range(0, 12, 2))
    parts = mac.split(":")
    if len(parts) != 6:
        raise ValueError(f"Неверный MAC: {mac}")
    return [int(p, 16) for p in parts]

def is_valid_mac(mac: str) -> bool:
    try:
        _parse(mac)
        return True
    except Exception:
        return False

def normalize_mac(mac: str) -> str:
    return ":".join(f"{b:02X}" for b in _parse(mac))

def mac_to_int(mac: str) -> int:
    n = 0
    for b in _parse(mac):
        n = (n << 8) | b
    return n

def int_to_mac(n: int) -> str:
    parts = []
    for _ in range(6):
        parts.append(f"{n & 0xFF:02X}")
        n >>= 8
    return ":".join(reversed(parts))

def is_multicast(mac: str) -> bool:
    return (_parse(mac)[0] & 0x01) == 1

def is_locally_administered(mac: str) -> bool:
    return (_parse(mac)[0] & 0x02) == 2

def oui(mac: str) -> str:
    p = _parse(mac)
    return ":".join(f"{b:02X}" for b in p[:3])

def generate_random_mac(locally_administered: bool = True) -> str:
    b = [random.randint(0, 255) for _ in range(6)]
    if locally_administered:
        b[0] = (b[0] | 0x02) & 0xFE   # U/L=1, I/G=0
    else:
        b[0] = b[0] & 0xFC
    return ":".join(f"{x:02X}" for x in b)

if __name__ == "__main__":
    print(is_valid_mac("aa:bb:cc:dd:ee:ff"))
    print(is_valid_mac("ZZ:ZZ:ZZ:ZZ:ZZ:ZZ"))
    print(normalize_mac("aa-bb-cc-dd-ee-ff"))
    print(mac_to_int("00:00:00:00:00:01"))
    print(int_to_mac(1))
    print(is_multicast("01:00:5e:00:00:01"))
    print(oui("AA:BB:CC:DD:EE:FF"))
    mac = generate_random_mac()
    print(f"random: {mac}, locally_administered={is_locally_administered(mac)}")
