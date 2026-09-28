class NATTable:
    def __init__(self, public_ip: str, port_start: int = 10000):
        self._pub_ip = public_ip
        self._next_port = port_start
        self._out = {}   # (priv_ip,priv_port,dst_ip,dst_port) -> pub_port
        self._in  = {}   # pub_port -> (priv_ip, priv_port)
        self._meta = {}  # pub_port -> full record

    def translate_out(self, src_ip, src_port, dst_ip, dst_port):
        key = (src_ip, src_port, dst_ip, dst_port)
        if key in self._out:
            return self._pub_ip, self._out[key]
        pp = self._next_port
        self._next_port += 1
        self._out[key] = pp
        self._in[pp] = (src_ip, src_port)
        self._meta[pp] = {"priv_ip": src_ip, "priv_port": src_port,
                          "pub_port": pp, "dst_ip": dst_ip, "dst_port": dst_port}
        return self._pub_ip, pp

    def translate_in(self, dst_port: int):
        return self._in.get(dst_port)

    def table(self) -> list:
        return list(self._meta.values())

if __name__ == "__main__":
    nat = NATTable(public_ip="203.0.113.1", port_start=10000)
    pub_ip, pub_port = nat.translate_out("192.168.1.10", 54321, "8.8.8.8", 53)
    print(pub_ip, pub_port)
    print(nat.translate_in(pub_port))
    print(nat.table())
