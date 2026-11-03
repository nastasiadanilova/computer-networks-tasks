"""
Задание 30. Симулятор traceroute.

Симулирует прохождение пакетов по маршруту с TTL-декрементом.
В учебной среде без raw-сокетов используется детерминированная симуляция.
"""

import random
import socket
import time


# Предопределенный маршрут для симуляции (имитирует реальную топологию)
_SIM_ROUTE = [
    "192.168.1.1",
    "10.0.0.1",
    "172.16.0.1",
    "203.0.113.1",
    "198.51.100.5",
    "8.8.8.8",
]


def traceroute(destination: str, max_hops: int = 30) -> list:
    """
    Симулирует traceroute до destination.

    В реальной реализации использовались бы raw-сокеты с ICMP TTL-exceeded.
    Здесь используется детерминированная симуляция для учебных целей.

    Returns:
        Список словарей {"hop": int, "ip": str, "rtt_ms": float}
    """
    hops = []
    rng = random.Random(hash(destination) & 0xFFFFFFFF)

    # Определяем маршрут: для известного адреса используем симуляцию
    route = list(_SIM_ROUTE)
    if destination not in route:
        route.append(destination)

    base_rtt = 0.3
    for ttl in range(1, min(max_hops + 1, len(route) + 1)):
        ip = route[ttl - 1]
        # RTT растет с числом переходов плюс случайный джиттер
        rtt = base_rtt * ttl + rng.uniform(0.1, 2.5)
        hops.append({"hop": ttl, "ip": ip, "rtt_ms": round(rtt, 2)})
        if ip == destination:
            break

    return hops


if __name__ == "__main__":
    print("Traceroute to 8.8.8.8:")
    for h in traceroute("8.8.8.8", max_hops=5):
        print(f"  {h['hop']:2d}  {h['ip']:<18s}  {h['rtt_ms']:.2f} ms")
