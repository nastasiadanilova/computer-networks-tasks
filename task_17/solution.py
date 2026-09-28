import socket, threading, sys

BUFSIZE = 4096

def forward(src, dst, label):
    total = 0
    try:
        while True:
            data = src.recv(BUFSIZE)
            if not data:
                break
            dst.sendall(data)
            total += len(data)
    except Exception:
        pass
    finally:
        print(f"[proxy] {label}: {total} bytes")
        try: dst.shutdown(socket.SHUT_WR)
        except Exception: pass

def handle(client_sock, target_host, target_port):
    try:
        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target.connect((target_host, target_port))
        t1 = threading.Thread(target=forward, args=(client_sock, target, "client→target"), daemon=True)
        t2 = threading.Thread(target=forward, args=(target, client_sock, "target→client"), daemon=True)
        t1.start(); t2.start()
        t1.join(); t2.join()
    finally:
        client_sock.close()

def main(local_port, target_host, target_port):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", local_port))
    srv.listen(10)
    print(f"[proxy] listening ::{local_port} → {target_host}:{target_port}")
    try:
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle, args=(conn, target_host, target_port), daemon=True).start()
    except KeyboardInterrupt:
        print("[proxy] stopped")
    finally:
        srv.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: proxy.py <local_port> <target_host> <target_port>")
        sys.exit(1)
    main(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
