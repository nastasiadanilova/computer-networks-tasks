import ipaddress, math

def vlsm_allocate(network: str, segments: list) -> list:
    net = ipaddress.ip_network(network, strict=True)
    segs = sorted(segments, key=lambda x: -x[1])
    available = [net]
    result = []
    for name, n in segs:
        bits = math.ceil(math.log2(n + 2))
        prefix = 32 - bits
        available.sort(key=lambda b: b.prefixlen, reverse=True)
        chosen = next((b for b in available if b.prefixlen <= prefix), None)
        if not chosen:
            raise ValueError(f"no space for '{name}' ({n} hosts)")
        available.remove(chosen)
        if chosen.prefixlen < prefix:
            subs = list(chosen.subnets(new_prefix=prefix))
            used, rest = subs[0], subs[1:]
            available.extend(rest)
        else:
            used = chosen
        hosts = list(used.hosts())
        usable = len(hosts)
        result.append({"name": name, "required": n,
                        "allocated": str(used),
                        "first_host": str(hosts[0]),
                        "last_host": str(hosts[-1]),
                        "usable": usable, "waste": usable - n})
    return result

if __name__ == "__main__":
    segs = [("Sales", 120), ("IT", 55), ("HR", 25), ("Link1", 2)]
    for r in vlsm_allocate("10.0.0.0/20", segs):
        print(r)
