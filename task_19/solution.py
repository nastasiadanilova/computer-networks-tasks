class VLANSwitch:
    def __init__(self):
        self._vlans = {}       # vlan_id -> name
        self._access = {}      # port -> vlan_id
        self._trunk = {}       # port -> set(vlan_id)
        self._mac_table = {}   # mac -> (port, vlan_id)

    def add_vlan(self, vlan_id: int, name: str):
        self._vlans[vlan_id] = name

    def set_access(self, port: str, vlan_id: int):
        self._access[port] = vlan_id
        self._trunk.pop(port, None)

    def set_trunk(self, port: str, allowed_vlans: list):
        self._trunk[port] = set(allowed_vlans)
        self._access.pop(port, None)

    def _port_vlan(self, port):
        if port in self._access:
            return self._access[port]
        return None  # trunk не имеет одного VLAN

    def _egress_ports(self, src_port, vlan_id):
        ports = []
        for p in list(self._access) + list(self._trunk):
            if p == src_port:
                continue
            if p in self._access and self._access[p] == vlan_id:
                ports.append(p)
            elif p in self._trunk and vlan_id in self._trunk[p]:
                ports.append(p)
        return ports

    def send_frame(self, src_port: str, dst_mac: str, payload: str) -> list:
        vlan_id = self._port_vlan(src_port)
        if vlan_id is None:
            return []

        # изучаем src MAC (используем payload как "заглушку" для src mac)
        # для демонстрации src_mac берем из src_port
        src_mac = f"mac-{src_port}"
        self._mac_table[src_mac] = (src_port, vlan_id)

        # unicast lookup
        if dst_mac in self._mac_table:
            dst_port, dst_vlan = self._mac_table[dst_mac]
            if dst_vlan == vlan_id:
                return [dst_port]
            return []

        # flooding
        return self._egress_ports(src_port, vlan_id)

    def mac_table(self) -> dict:
        return dict(self._mac_table)

if __name__ == "__main__":
    sw = VLANSwitch()
    sw.add_vlan(10, "Sales"); sw.add_vlan(20, "IT")
    sw.set_access("fa0/1", 10); sw.set_access("fa0/2", 10); sw.set_access("fa0/3", 20)
    print(sw.send_frame("fa0/1", "ff:ff:ff:ff:ff:ff", "ARP request"))
    print(sw.send_frame("fa0/3", "ff:ff:ff:ff:ff:ff", "ARP request"))
