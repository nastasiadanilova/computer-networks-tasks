import ipaddress, time

class ACL:
    def __init__(self):
        self._rules = []
        self._log = []

    def add_rule(self, action, proto, src, dst, dst_port=None, description=""):
        self._rules.append({
            "action": action, "proto": proto,
            "src": src, "dst": dst,
            "dst_port": dst_port, "description": description,
        })

    def _match(self, rule, pkt) -> bool:
        if rule["proto"] != "any" and rule["proto"] != pkt["proto"]:
            return False
        def in_net(addr, net_str):
            if net_str == "any":
                return True
            return ipaddress.ip_address(addr) in ipaddress.ip_network(net_str, strict=False)
        if not in_net(pkt["src"], rule["src"]):
            return False
        if not in_net(pkt["dst"], rule["dst"]):
            return False
        if rule["dst_port"] is not None and rule["dst_port"] != pkt.get("dst_port"):
            return False
        return True

    def check(self, packet: dict) -> dict:
        for i, rule in enumerate(self._rules):
            if self._match(rule, packet):
                result = {"action": rule["action"], "rule_index": i,
                          "description": rule["description"]}
                self._log.append({"ts": round(time.time(),3),
                                  "packet": packet, "result": result})
                return result
        result = {"action": "deny", "rule_index": -1, "description": "implicit deny"}
        self._log.append({"ts": round(time.time(),3), "packet": packet, "result": result})
        return result

    def log(self) -> list:
        return self._log

if __name__ == "__main__":
    acl = ACL()
    acl.add_rule("permit","tcp","203.0.113.5/32","192.168.1.100/32",22,"admin SSH")
    acl.add_rule("deny",  "tcp","any",           "192.168.1.100/32",22,"block SSH")
    acl.add_rule("permit","any","192.168.1.0/24","any",None,         "LAN out")
    for p in [
        {"proto":"tcp","src":"203.0.113.5","dst":"192.168.1.100","dst_port":22},
        {"proto":"tcp","src":"1.2.3.4",    "dst":"192.168.1.100","dst_port":22},
        {"proto":"udp","src":"192.168.1.5","dst":"8.8.8.8",      "dst_port":53},
        {"proto":"tcp","src":"5.5.5.5",    "dst":"8.8.8.8",      "dst_port":80},
    ]:
        print(acl.check(p))
