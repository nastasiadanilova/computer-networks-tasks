"""
Задание 39. Симулятор SNMP MIB.

SNMP-агент с деревом OID: GET, SET, GETNEXT, WALK.
OID сортируются лексикографически по числовым компонентам.
"""


def _oid_key(oid: str) -> tuple:
    """Преобразует строку OID в кортеж чисел для сравнения."""
    return tuple(int(x) for x in oid.split("."))


class SNMPAgent:
    """
    Симулятор SNMP-агента с деревом MIB.

    MIB хранится как плоский словарь OID -> {value, writable}.
    GETNEXT и WALK используют лексикографический обход (по числовым компонентам).
    """

    def __init__(self):
        # OID -> {"value": any, "writable": bool}
        self._mib: dict = {}

    def register(self, oid: str, value, writable: bool = False):
        """Регистрирует OID в MIB."""
        self._mib[oid] = {"value": value, "writable": writable}

    def get(self, oid: str):
        """
        Возвращает значение OID.

        Raises:
            KeyError: OID не найден в MIB.
        """
        if oid not in self._mib:
            raise KeyError(f"OID {oid} не найден в MIB")
        return self._mib[oid]["value"]

    def set(self, oid: str, value) -> bool:
        """
        Устанавливает значение OID.

        Returns:
            True при успехе, False если OID не writable или не существует.
        """
        entry = self._mib.get(oid)
        if entry is None or not entry["writable"]:
            return False
        entry["value"] = value
        return True

    def getnext(self, oid: str):
        """
        Возвращает следующий OID в лексикографическом порядке.

        Returns:
            (next_oid, value) или (None, None) если достигнут конец MIB.
        """
        sorted_oids = sorted(self._mib.keys(), key=_oid_key)
        target_key = _oid_key(oid)
        for o in sorted_oids:
            if _oid_key(o) > target_key:
                return (o, self._mib[o]["value"])
        return (None, None)

    def walk(self, start_oid: str) -> list:
        """
        Обходит все OID, начинающиеся с start_oid (поддерево).

        Returns:
            Список кортежей (oid, value) в лексикографическом порядке.
        """
        prefix = start_oid.rstrip(".")
        result = []
        for oid in sorted(self._mib.keys(), key=_oid_key):
            if oid == prefix or oid.startswith(prefix + "."):
                result.append((oid, self._mib[oid]["value"]))
        return result


if __name__ == "__main__":
    agent = SNMPAgent()
    agent.register("1.3.6.1.2.1.1.1.0", "Linux Router 2.6", writable=False)
    agent.register("1.3.6.1.2.1.1.5.0", "router01",         writable=True)
    agent.register("1.3.6.1.2.1.2.1.0", 3,                  writable=False)

    print(agent.get("1.3.6.1.2.1.1.1.0"))
    agent.set("1.3.6.1.2.1.1.5.0", "core-router")
    print(agent.get("1.3.6.1.2.1.1.5.0"))

    for oid, val in agent.walk("1.3.6.1.2.1.1"):
        print(f"  {oid} = {val}")
