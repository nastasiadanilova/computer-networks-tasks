"""
Задание 29. Операции с IPv6-адресами.

Функции для работы с IPv6: развертывание, сжатие, проверка подсети.
"""

import ipaddress


def expand_ipv6(addr: str) -> str:
    """Развертывает сокращенный IPv6-адрес в полную форму (8 групп по 4 hex)."""
    full = ipaddress.ip_address(addr).exploded
    return full


def compress_ipv6(addr: str) -> str:
    """Сжимает IPv6-адрес в сокращенную форму по RFC 5952."""
    return ipaddress.ip_address(addr).compressed


def ipv6_in_subnet(addr: str, prefix: str) -> bool:
    """Проверяет, принадлежит ли IPv6-адрес указанной подсети."""
    return ipaddress.ip_address(addr) in ipaddress.ip_network(prefix, strict=False)


if __name__ == "__main__":
    print(expand_ipv6("2001:db8::1"))
    print(expand_ipv6("::1"))
    print(compress_ipv6("2001:0db8:0000:0000:0000:0000:0000:0001"))
    print(compress_ipv6("0000:0000:0000:0000:0000:0000:0000:0001"))
    print(ipv6_in_subnet("2001:db8::5", "2001:db8::/32"))
    print(ipv6_in_subnet("2001:db9::1", "2001:db8::/32"))
