import re
from collections import defaultdict

def analyze_log(lines: list) -> dict:
    PAT = re.compile(
        r"(\S+ \S+)\s+(\w+)\s+([\d.]+):(\d+)\s+->\s+([\d.]+):(\d+)\s+len=(\d+)"
    )
    total_pkts = 0
    total_bytes = 0
    by_proto = defaultdict(lambda: {"packets": 0, "bytes": 0})
    src_cnt = defaultdict(int)
    dst_cnt = defaultdict(int)
    dport_cnt = defaultdict(int)

    for line in lines:
        m = PAT.search(line)
        if not m:
            continue
        _, proto, src_ip, src_port, dst_ip, dst_port, length = m.groups()
        length = int(length)
        total_pkts += 1
        total_bytes += length
        by_proto[proto]["packets"] += 1
        by_proto[proto]["bytes"] += length
        src_cnt[src_ip] += 1
        dst_cnt[dst_ip] += 1
        dport_cnt[int(dst_port)] += 1

    def top(d, n=3):
        return sorted(d.items(), key=lambda x: -x[1])[:n]

    return {
        "total_packets": total_pkts,
        "total_bytes": total_bytes,
        "by_proto": dict(by_proto),
        "top_src": top(src_cnt),
        "top_dst": top(dst_cnt),
        "top_dst_port": top(dport_cnt),
    }

if __name__ == "__main__":
    import pprint
    lines = [
        "2026-09-01 10:00:01 TCP 192.168.1.10:54321 -> 8.8.8.8:443 len=1400",
        "2026-09-01 10:00:02 TCP 192.168.1.10:54322 -> 8.8.8.8:443 len=1400",
        "2026-09-01 10:00:03 UDP 192.168.1.11:53001 -> 8.8.4.4:53  len=120",
        "2026-09-01 10:00:04 TCP 192.168.1.12:60001 -> 10.0.0.1:22 len=200",
    ]
    pprint.pprint(analyze_log(lines))
