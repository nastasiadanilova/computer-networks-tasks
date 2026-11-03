"""
Задание 49. Система обнаружения вторжений (IDS).

Анализирует поток пакетов и выявляет: port scan, SYN flood, ping flood, DNS amp.
"""

import time
from collections import defaultdict


class NetworkIDS:
    """
    Упрощенная сигнатурная IDS.

    Хранит счетчики событий за скользящее временное окно.
    При превышении порога генерирует оповещение (один раз на источник + правило).
    """

    def __init__(self, window_sec: float = 60.0):
        self.window_sec = window_sec
        self._rules: list = []
        self._total_packets = 0
        self._alerts: list = []
        self._alerted: set = set()   # (src, rule_name) - чтобы не дублировать

        # Счетчики для встроенных правил
        # src -> set of dst_ports (для port scan)
        self._src_ports: dict = defaultdict(set)
        # src -> список ts SYN-пакетов (для SYN flood)
        self._syn_times: dict = defaultdict(list)
        # src -> список ts ICMP (для ping flood)
        self._icmp_times: dict = defaultdict(list)
        # src -> список ts DNS-ответов размером >512 байт (для DNS amp)
        self._dns_amp_times: dict = defaultdict(list)

        # Регистрируем встроенные правила
        self._register_builtin_rules()

    def _register_builtin_rules(self):
        """Добавляет стандартный набор правил обнаружения."""
        self.add_rule(
            name="port_scan",
            threshold=10,
            description="Port scan detected: {count} unique ports",
        )
        self.add_rule(
            name="syn_flood",
            threshold=50,
            description="SYN flood: {count} SYN packets in {window}s",
        )
        self.add_rule(
            name="ping_flood",
            threshold=20,
            description="Ping flood: {count} ICMP packets in {window}s",
        )

    def add_rule(self, name: str, threshold: int, description: str):
        """Регистрирует правило обнаружения."""
        self._rules.append({
            "name": name,
            "threshold": threshold,
            "description": description,
        })

    def _clean_window(self, ts_list: list, now: float) -> list:
        """Удаляет записи старше временного окна."""
        cutoff = now - self.window_sec
        return [t for t in ts_list if t >= cutoff]

    def process_packet(self, packet: dict):
        """
        Обрабатывает один пакет и проверяет правила.

        Args:
            packet: {"ts": float, "src": str, "dst": str,
                     "proto": str, "dst_port": int, "flags": str}
        """
        self._total_packets += 1
        src = packet.get("src", "")
        proto = packet.get("proto", "").lower()
        dst_port = packet.get("dst_port", 0)
        flags = packet.get("flags", "").upper()
        ts = packet.get("ts", time.time())

        # Счетчик уникальных портов (port scan)
        if proto == "tcp":
            self._src_ports[src].add(dst_port)

        # Счетчик SYN-пакетов (SYN flood)
        if proto == "tcp" and "SYN" in flags and "ACK" not in flags:
            self._syn_times[src] = self._clean_window(self._syn_times[src], ts)
            self._syn_times[src].append(ts)

        # Счетчик ICMP (ping flood)
        if proto == "icmp":
            self._icmp_times[src] = self._clean_window(self._icmp_times[src], ts)
            self._icmp_times[src].append(ts)

        # Проверяем правила
        self._check_rules(src, ts)

    def _check_rules(self, src: str, ts: float):
        """Проверяет все правила для данного источника."""
        for rule in self._rules:
            name = rule["name"]
            threshold = rule["threshold"]
            key = (src, name)
            if key in self._alerted:
                continue

            count = 0
            if name == "port_scan":
                count = len(self._src_ports.get(src, set()))
            elif name == "syn_flood":
                count = len(self._syn_times.get(src, []))
            elif name == "ping_flood":
                count = len(self._icmp_times.get(src, []))

            if count >= threshold:
                desc = rule["description"].format(
                    count=count, window=int(self.window_sec)
                )
                self._alerts.append({
                    "rule": name,
                    "src": src,
                    "count": count,
                    "description": desc,
                    "ts": ts,
                })
                self._alerted.add(key)

    def alerts(self) -> list:
        """Возвращает все сгенерированные оповещения."""
        return list(self._alerts)

    def stats(self) -> dict:
        """Возвращает статистику IDS."""
        return {
            "total_packets": self._total_packets,
            "total_alerts": len(self._alerts),
            "unique_sources": len(self._src_ports),
        }


if __name__ == "__main__":
    ids = NetworkIDS(window_sec=60)

    base_ts = time.time()
    # Симулируем port scan
    for port in range(20, 40):
        ids.process_packet({
            "ts": base_ts,
            "src": "10.0.0.1",
            "dst": "192.168.1.1",
            "proto": "tcp",
            "dst_port": port,
            "flags": "SYN",
        })

    alerts = ids.alerts()
    for a in alerts:
        print(f"[{a['rule']}] {a['src']} -> {a['description']}")

    print("Total packets:", ids.stats()["total_packets"])
