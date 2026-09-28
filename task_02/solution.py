import ipaddress

def ip_class(ip: str) -> dict:
    addr = ipaddress.ip_address(ip)
    first = int(ip.split(".")[0])
    if first == 127:
        cls, mask, ip_type = "A", "255.0.0.0", "loopback"
    elif 1 <= first <= 126:
        cls, mask = "A", "255.0.0.0"
        ip_type = "private" if addr.is_private else "public"
    elif 128 <= first <= 191:
        cls, mask = "B", "255.255.0.0"
        ip_type = "private" if addr.is_private else "public"
    elif 192 <= first <= 223:
        cls, mask = "C", "255.255.255.0"
        ip_type = "private" if addr.is_private else "public"
    elif 224 <= first <= 239:
        cls, mask, ip_type = "D", "240.0.0.0", "multicast"
    else:
        cls, mask, ip_type = "E", "reserved", "reserved"
    return {"ip": ip, "class": cls, "type": ip_type,
            "default_mask": mask, "first_octet": first}

if __name__ == "__main__":
    for a in ["192.168.1.1", "10.0.0.1", "8.8.8.8", "224.0.0.1", "127.0.0.1"]:
        print(ip_class(a))
