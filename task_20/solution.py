import re

def parse_cisco_config(text: str) -> dict:
    result = {
        "hostname": None, "interfaces": {},
        "static_routes": [], "acls": {},
        "ntp_server": None, "dns_servers": [],
    }
    lines = text.splitlines()
    current_iface = None
    current_acl = None

    for line in lines:
        s = line.strip()
        # hostname
        if m := re.match(r"^hostname\s+(\S+)", s):
            result["hostname"] = m.group(1)
        # interface
        elif m := re.match(r"^interface\s+(\S+)", s):
            current_iface = m.group(1)
            current_acl = None
            result["interfaces"][current_iface] = {
                "ip": None, "mask": None,
                "description": None, "shutdown": False
            }
        elif current_iface and not line.startswith("!") and line.startswith(" "):
            iface = result["interfaces"][current_iface]
            if m := re.match(r"\s+ip address\s+([\d.]+)\s+([\d.]+)", line):
                iface["ip"], iface["mask"] = m.group(1), m.group(2)
            elif m := re.match(r"\s+description\s+(.+)", line):
                iface["description"] = m.group(1).strip()
            elif re.match(r"\s+shutdown", line):
                iface["shutdown"] = True
            elif re.match(r"\s+no shutdown", line):
                iface["shutdown"] = False
        # static route
        elif m := re.match(r"^ip route\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", s):
            result["static_routes"].append(
                {"network": m.group(1), "mask": m.group(2), "next_hop": m.group(3)})
            current_iface = None
        # ACL
        elif m := re.match(r"^ip access-list \w+ (\S+)", s):
            current_acl = m.group(1)
            current_iface = None
            result["acls"][current_acl] = []
        elif current_acl and line.startswith(" "):
            result["acls"][current_acl].append(s)
        # NTP
        elif m := re.match(r"^ntp server\s+(\S+)", s):
            result["ntp_server"] = m.group(1)
        # DNS
        elif m := re.match(r"^ip name-server\s+([\d.]+)", s):
            result["dns_servers"].append(m.group(1))
        elif s.startswith("!"):
            current_iface = None; current_acl = None

    return result

if __name__ == "__main__":
    import pprint
    pprint.pprint(parse_cisco_config(open("example.cfg").read()))
