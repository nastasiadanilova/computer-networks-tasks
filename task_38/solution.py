"""
Задание 38. Симулятор MPLS-коммутации меток.

Label Switching Router с операциями PUSH/SWAP/POP над стеком меток.
"""


class MPLSRouter:
    """
    Симулятор Label Switching Router (LSR).

    LFIB (Label Forwarding Information Base) хранит правила обработки меток:
      PUSH  - добавить метку в стек (для входного трафика без метки)
      SWAP  - заменить верхнюю метку (транзитный LSR)
      POP   - снять верхнюю метку (последний LSR, Penultimate Hop Popping)
    """

    def __init__(self, name: str):
        self.name = name
        # in_label -> {"action": str, "out_label": int|None, "out_interface": str}
        self._lfib: dict = {}

    def add_lfib_entry(
        self,
        in_label,           # None означает пакет без метки (IP-пакет на входе)
        action: str,
        out_label,          # None для POP
        out_interface: str,
    ):
        """Добавляет запись в таблицу LFIB."""
        if action not in ("PUSH", "SWAP", "POP"):
            raise ValueError(f"Неизвестное действие MPLS: {action}")
        self._lfib[in_label] = {
            "action": action,
            "out_label": out_label,
            "out_interface": out_interface,
        }

    def forward(self, packet: dict, in_label=None) -> dict:
        """
        Обрабатывает пакет согласно LFIB.

        Args:
            packet: {"src", "dst", "label_stack": list[int], "payload"}
            in_label: метка для поиска в LFIB (None = входящий IP-пакет)

        Returns:
            Обновленный пакет с полем out_interface и измененным label_stack.

        Raises:
            KeyError: если метка не найдена в LFIB.
        """
        if in_label not in self._lfib:
            raise KeyError(f"Метка {in_label} не найдена в LFIB маршрутизатора {self.name}")

        entry = self._lfib[in_label]
        action = entry["action"]
        out_label = entry["out_label"]
        out_iface = entry["out_interface"]

        stack = list(packet.get("label_stack", []))

        if action == "PUSH":
            stack.insert(0, out_label)
        elif action == "SWAP":
            if stack:
                stack[0] = out_label
            else:
                stack = [out_label]
        elif action == "POP":
            if stack:
                stack.pop(0)

        pkt = dict(packet)
        pkt["label_stack"] = stack
        pkt["out_interface"] = out_iface
        pkt["last_action"] = action
        return pkt


if __name__ == "__main__":
    r1 = MPLSRouter("R1")
    r1.add_lfib_entry(in_label=None,  action="PUSH", out_label=100, out_interface="eth1")
    r1.add_lfib_entry(in_label=100,   action="SWAP", out_label=200, out_interface="eth2")
    r1.add_lfib_entry(in_label=200,   action="POP",  out_label=None, out_interface="eth3")

    pkt = {"src": "10.0.0.1", "dst": "10.0.0.2", "label_stack": [], "payload": "data"}

    pkt = r1.forward(pkt, in_label=None)
    print(pkt["label_stack"], "->", pkt["out_interface"])

    pkt = r1.forward(pkt, in_label=100)
    print(pkt["label_stack"], "->", pkt["out_interface"])

    pkt = r1.forward(pkt, in_label=200)
    print(pkt["label_stack"], "->", pkt["out_interface"])
