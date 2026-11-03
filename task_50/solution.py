"""
Задание 50. Симулятор SDN-контроллера (OpenFlow-подобный).

Flow table с приоритетами, match-action обработкой пакетов и счетчиками.
"""


class FlowRule:
    """
    Правило потока (Flow Rule) в таблице OpenFlow-коммутатора.

    Поля match: src_ip, dst_ip, proto, dst_port, in_port (пустой match = wildcard).
    Действия (action): "forward:PORT" | "drop" | "flood".
    """

    def __init__(self, priority: int, match: dict, action: str):
        self.priority = priority
        self.match = match
        self.action = action
        self.hits = 0

    def matches(self, packet: dict) -> bool:
        """
        Проверяет, соответствует ли пакет правилу.

        Пустой словарь match - wildcard (совпадает с любым пакетом).
        """
        for field, value in self.match.items():
            if packet.get(field) != value:
                return False
        return True

    def __repr__(self) -> str:
        return f"FlowRule(priority={self.priority}, match={self.match}, action={self.action})"


class SDNSwitch:
    """
    OpenFlow-подобный программный коммутатор с flow table.

    Пакет обрабатывается первым совпадающим правилом (по убыванию приоритета).
    Если правило не найдено - пакет отправляется контроллеру (packet_in), здесь flood.
    """

    def __init__(self, switch_id: str):
        self.switch_id = switch_id
        self._flow_table: list = []     # список FlowRule, отсортированный по priority

    def install_rule(self, rule: FlowRule):
        """Устанавливает правило в flow table (сортировка по убыванию приоритета)."""
        self._flow_table.append(rule)
        self._flow_table.sort(key=lambda r: r.priority, reverse=True)

    def clear_rules(self):
        """Очищает flow table."""
        self._flow_table.clear()

    def process_packet(self, packet: dict) -> str:
        """
        Обрабатывает пакет: ищет первое совпадающее правило.

        Args:
            packet: {"src_ip", "dst_ip", "proto", "dst_port", "in_port", ...}

        Returns:
            Строка действия: "forward:1", "drop", "flood" или "packet_in" (нет правила).
        """
        for rule in self._flow_table:
            if rule.matches(packet):
                rule.hits += 1
                return rule.action

        # Table miss: отправляем контроллеру
        return "packet_in"

    def flow_stats(self) -> list:
        """Возвращает статистику по всем правилам."""
        return [
            {
                "priority": r.priority,
                "match": r.match,
                "action": r.action,
                "hits": r.hits,
            }
            for r in self._flow_table
        ]


class SDNController:
    """
    SDN-контроллер: управляет группой коммутаторов.

    Хранит реестр коммутаторов и загружает в них наборы правил (политики).
    """

    def __init__(self):
        self._switches: dict = {}   # switch_id -> SDNSwitch

    def register_switch(self, switch: SDNSwitch):
        """Регистрирует коммутатор в контроллере."""
        self._switches[switch.switch_id] = switch

    def push_policy(self, switch_id: str, rules: list):
        """
        Загружает набор правил на указанный коммутатор.

        Заменяет текущую flow table новыми правилами.
        """
        sw = self._switches.get(switch_id)
        if sw is None:
            raise KeyError(f"Коммутатор {switch_id} не зарегистрирован")
        sw.clear_rules()
        for rule in rules:
            sw.install_rule(rule)

    def get_switch(self, switch_id: str) -> SDNSwitch:
        """Возвращает коммутатор по ID."""
        return self._switches[switch_id]


if __name__ == "__main__":
    sw = SDNSwitch("sw1")
    ctrl = SDNController()
    ctrl.register_switch(sw)

    rules = [
        FlowRule(priority=100, match={"dst_ip": "10.0.0.1"}, action="forward:1"),
        FlowRule(priority=90,  match={"proto": "icmp"},       action="drop"),
        FlowRule(priority=1,   match={},                      action="flood"),
    ]
    ctrl.push_policy("sw1", rules)

    pkts = [
        {"src_ip": "10.0.0.5", "dst_ip": "10.0.0.1", "proto": "tcp",  "dst_port": 80},
        {"src_ip": "10.0.0.5", "dst_ip": "10.0.0.2", "proto": "icmp", "dst_port": 0},
        {"src_ip": "10.0.0.5", "dst_ip": "10.0.0.9", "proto": "udp",  "dst_port": 53},
    ]
    for pkt in pkts:
        action = sw.process_packet(pkt)
        print(f"{pkt['dst_ip']} / {pkt['proto']:4s} -> {action}")

    print()
    for stat in sw.flow_stats():
        print(f"  priority={stat['priority']} hits={stat['hits']} action={stat['action']}")
