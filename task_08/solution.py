import time

class ARPTable:
    def __init__(self, ttl: float = 300):
        self._ttl = ttl
        self._table = {}   # ip -> (mac, expires_at)

    def add(self, ip: str, mac: str):
        self._table[ip] = (mac.lower(), time.time() + self._ttl)

    def lookup(self, ip: str):
        if ip not in self._table:
            return None
        mac, exp = self._table[ip]
        if time.time() > exp:
            del self._table[ip]
            return None
        return mac

    def expire(self):
        now = time.time()
        self._table = {ip: v for ip, v in self._table.items() if v[1] > now}

    def dump(self) -> list:
        now = time.time()
        return [{"ip": ip, "mac": mac, "ttl_left": round(exp - now, 2)}
                for ip, (mac, exp) in self._table.items() if exp > now]

if __name__ == "__main__":
    arp = ARPTable(ttl=2)
    arp.add("192.168.1.1", "AA:BB:CC:DD:EE:FF")
    print(arp.lookup("192.168.1.1"))
    time.sleep(3)
    arp.expire()
    print(arp.lookup("192.168.1.1"))
    print(arp.dump())
