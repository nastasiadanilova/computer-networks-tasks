import ipaddress

class Router:
    def __init__(self):
        self._routes = []  # list of (network_obj, next_hop, iface, metric)

    def add_route(self, network: str, next_hop, iface: str, metric: int = 1):
        net = ipaddress.ip_network(network, strict=False)
        self._routes.append((net, next_hop, iface, metric))

    def remove_route(self, network: str):
        net = ipaddress.ip_network(network, strict=False)
        self._routes = [r for r in self._routes if r[0] != net]

    def lookup(self, dst_ip: str) -> dict:
        ip = ipaddress.ip_address(dst_ip)
        best = None
        for net, nh, iface, metric in self._routes:
            if ip in net:
                if best is None or net.prefixlen > best[0].prefixlen:
                    best = (net, nh, iface, metric)
        if best is None:
            raise ValueError(f"No route to {dst_ip}")
        return {"dst": dst_ip, "matched_route": str(best[0]),
                "next_hop": best[1], "iface": best[2], "metric": best[3]}

    def show_table(self) -> list:
        return [{"network": str(n), "next_hop": nh,
                 "iface": iface, "metric": m}
                for n, nh, iface, m in sorted(self._routes,
                    key=lambda x: -x[0].prefixlen)]

if __name__ == "__main__":
    r = Router()
    r.add_route("192.168.1.0/24", None, "eth0")
    r.add_route("10.0.0.0/8", "192.168.1.1", "eth1", metric=10)
    r.add_route("0.0.0.0/0", "10.0.0.1", "eth0", metric=1)
    print(r.lookup("192.168.1.55"))
    print(r.lookup("8.8.8.8"))
    for row in r.show_table():
        print(row)
