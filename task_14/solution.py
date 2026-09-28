import ipaddress, time

class DHCPServer:
    def __init__(self, pool_network: str, lease_time=86400, dns=None, gw=None):
        net = ipaddress.ip_network(pool_network, strict=True)
        hosts = list(net.hosts())
        self._pool = [str(h) for h in hosts[1:]]
        self._gw = gw or str(hosts[0])
        self._dns = dns
        self._lease_time = lease_time
        self._leases = {}   # mac -> {ip, expires}
        self._offers = {}   # mac -> ip (предложенные, но не подтвержденные)
        self._used = set()  # занятые IP

    def _next_free(self):
        for ip in self._pool:
            if ip not in self._used:
                return ip
        return None

    def discover(self, mac: str) -> dict:
        mac = mac.lower()
        if mac in self._leases:
            ip = self._leases[mac]["ip"]
        elif mac in self._offers:
            ip = self._offers[mac]
        else:
            ip = self._next_free()
            if not ip:
                raise RuntimeError("Pool exhausted")
            self._offers[mac] = ip
        return {"offered_ip": ip, "lease_time": self._lease_time,
                "dns": self._dns, "gw": self._gw}

    def request(self, mac: str, requested_ip: str) -> dict:
        mac = mac.lower()
        offered = self._offers.get(mac) or (
            self._leases[mac]["ip"] if mac in self._leases else None)
        if offered != requested_ip or (requested_ip in self._used and self._leases.get(mac,{}).get("ip") != requested_ip):
            return {"status": "NAK", "reason": "IP not available"}
        self._used.add(requested_ip)
        self._offers.pop(mac, None)
        self._leases[mac] = {"ip": requested_ip,
                              "expires": time.time() + self._lease_time}
        return {"status": "ACK", "ip": requested_ip,
                "mac": mac, "lease_time": self._lease_time}

    def release(self, mac: str):
        mac = mac.lower()
        if mac in self._leases:
            self._used.discard(self._leases[mac]["ip"])
            del self._leases[mac]

    def leases(self) -> list:
        now = time.time()
        return [{"mac": m, "ip": v["ip"],
                 "ttl_left": round(v["expires"]-now)}
                for m, v in self._leases.items()]

    def available_count(self) -> int:
        return len([ip for ip in self._pool if ip not in self._used])

if __name__ == "__main__":
    srv = DHCPServer("192.168.100.0/28", lease_time=3600,
                     dns="8.8.8.8", gw="192.168.100.1")
    offer = srv.discover("aa:bb:cc:dd:ee:01")
    print(offer)
    ack = srv.request("aa:bb:cc:dd:ee:01", offer["offered_ip"])
    print(ack)
    print(srv.available_count())
