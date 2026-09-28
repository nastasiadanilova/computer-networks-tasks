class DNSResolver:
    def __init__(self):
        self._zone = {}
        self._cache = {}
        self._hits = 0
        self._misses = 0

    def load_zone(self, zone: dict):
        self._zone.update(zone)

    def resolve(self, name: str, rtype: str = "A", _depth: int = 0):
        if _depth > 10:
            return None
        key = (name, rtype)
        if key in self._cache:
            self._hits += 1
            return self._cache[key]
        self._misses += 1
        record = self._zone.get(name)
        if record is None:
            return None
        if rtype in record:
            result = record[rtype]
            self._cache[key] = result
            return result
        if "CNAME" in record:
            target = record["CNAME"][0]
            result = self.resolve(target, rtype, _depth + 1)
            if result:
                self._cache[key] = result
            return result
        return None

    def cache_stats(self) -> dict:
        return {"hits": self._hits, "misses": self._misses,
                "entries": len(self._cache)}

if __name__ == "__main__":
    d = DNSResolver()
    d.load_zone({
        "www.lab.local": {"A": ["10.0.0.10"]},
        "ftp.lab.local": {"CNAME": ["www.lab.local"]},
        "lab.local":     {"MX": [(10, "mail.lab.local")],
                          "TXT": ["v=spf1 include:lab.local ~all"]},
        "mail.lab.local":{"A": ["10.0.0.20"]},
    })
    print(d.resolve("ftp.lab.local", "A"))
    print(d.resolve("ftp.lab.local", "A"))
    print(d.resolve("lab.local", "MX"))
    print(d.cache_stats())
