import socket

HOST, PORT = "127.0.0.1", 9090

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[server] listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[server] connected: {addr}")
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    msg = data.decode().strip()
                    print(f"[server] recv: {msg}")
                    resp = msg.upper()
                    conn.sendall(resp.encode())
                    print(f"[server] sent: {resp}")

if __name__ == "__main__":
    main()

# client.py
import socket, sys

HOST, PORT = "127.0.0.1", 9090

def send(message: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[client] sent: {message}")
        s.sendall(message.encode())
        resp = s.recv(4096).decode()
        print(f"[client] got: {resp}")
        return resp

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "hello network"
    send(msg)
