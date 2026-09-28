import ipaddress

def subnet_calc(network: str, new_prefix: int) -> list:
    net = ipaddress.ip_network(network, strict=True)
    if new_prefix <= net.prefixlen:
        raise ValueError("new_prefix must be greater than current prefix")
    if new_prefix > 30:
        raise ValueError("new_prefix > 30 leaves no usable hosts")
    result = []
    for i, sub in enumerate(net.subnets(new_prefix=new_prefix)):
        hosts = list(sub.hosts())
        wc_int = 0xFFFFFFFF ^ int(sub.netmask)
        wc = str(ipaddress.ip_address(wc_int))
        result.append({
            "index": i,
            "network": str(sub),
            "netmask": str(sub.netmask),
            "wildcard": wc,
            "first_host": str(hosts[0]),
            "last_host": str(hosts[-1]),
            "broadcast": str(sub.broadcast_address),
            "total_hosts": sub.num_addresses,
            "usable_hosts": sub.num_addresses - 2,
        })
    return result

if __name__ == "__main__":
    for s in subnet_calc("192.168.1.0/24", 26):
        print(s)
