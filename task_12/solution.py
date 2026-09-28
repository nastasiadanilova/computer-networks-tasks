import math

def channel_stats(file_mb: float, bandwidth_mbps: float,
                  prop_delay_ms: float, packet_b: int,
                  ack_b: int = 40) -> dict:
    file_bytes = int(file_mb * 1_000_000)
    bw = bandwidth_mbps * 1_000_000
    prop = prop_delay_ms / 1000
    num_packets = math.ceil(file_bytes / packet_b)
    t_packet = (packet_b * 8) / bw
    t_ack = (ack_b * 8) / bw
    rtt = 2 * prop
    t_transmit = (file_bytes * 8) / bw
    t_sw = num_packets * (t_packet + rtt + t_ack)
    efficiency = (t_transmit / t_sw * 100) if t_sw else 0
    return {
        "file_bytes": file_bytes,
        "bandwidth_bps": int(bw),
        "prop_delay_s": prop,
        "packet_bytes": packet_b,
        "num_packets": num_packets,
        "t_transmit_s": round(t_transmit, 6),
        "t_packet_s": round(t_packet, 8),
        "t_ack_s": round(t_ack, 8),
        "rtt_s": round(rtt, 6),
        "t_stop_wait_s": round(t_sw, 4),
        "efficiency_pct": round(efficiency, 2),
    }

if __name__ == "__main__":
    s = channel_stats(file_mb=50, bandwidth_mbps=100,
                      prop_delay_ms=20, packet_b=1500)
    for k, v in s.items():
        print(f"{k}: {v}")
