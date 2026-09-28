def ip_to_binary(ip: str) -> str:
    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError(f"bad ip: {ip}")
    result = []
    for p in parts:
        n = int(p)
        if n < 0 or n > 255:
            raise ValueError(f"octet out of range: {p}")
        result.append(format(n, "08b"))
    return ".".join(result)

if __name__ == "__main__":
    print(ip_to_binary("192.168.1.1"))
    print(ip_to_binary("10.0.0.1"))
