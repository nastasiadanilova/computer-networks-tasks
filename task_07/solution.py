import socket, sys
from concurrent.futures import ThreadPoolExecutor

def grab_banner(host, port, timeout=1.0) -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            return s.recv(64).decode(errors="replace").split("\n")[0]
    except Exception:
        return ""

def check_port(host, port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        if s.connect_ex((host, port)) == 0:
            return port, True
    return port, False

def scan_ports(host: str, start: int, end: int,
               timeout: float = 0.5, workers: int = 200) -> list:
    results = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(check_port, host, p, timeout): p
                for p in range(start, end + 1)}
        for f in futs:
            port, is_open = f.result()
            if is_open:
                banner = grab_banner(host, port)
                results.append({"port": port, "state": "open", "banner": banner})
    return sorted(results, key=lambda x: x["port"])

if __name__ == "__main__":
    host  = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end   = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    found = scan_ports(host, start, end)
    print(f"{'PORT':<8}{'STATE':<10}BANNER")
    for r in found:
        print(f"{r['port']:<8}{'open':<10}{r['banner'][:60]}")
    if not found:
        print("No open ports found")
