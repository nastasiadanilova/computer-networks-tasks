import socket

HOST, PORT = "127.0.0.1", 9191
BUFSZ = 4096

def main():
    clients = {}
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"[server] UDP listening on {HOST}:{PORT}")
        while True:
            data, addr = s.recvfrom(BUFSZ)
            msg = data.decode().strip()
            if msg.startswith("JOIN:"):
                clients[addr] = msg[5:]
                print(f"[server] {clients[addr]} joined")
            elif msg == "LEAVE":
                nick = clients.pop(addr, str(addr))
                print(f"[server] {nick} left")
            elif msg.startswith("MSG:"):
                text = msg[4:]
                nick = clients.get(addr, str(addr))
                peers = [a for a in clients if a != addr]
                for peer in peers:
                    s.sendto(f"{nick}: {text}".encode(), peer)
                print(f"[server] {nick}: {text} -> broadcast to {len(peers)} peers")

if __name__ == "__main__":
    main()

# client.py
import socket, sys, time

HOST, PORT = "127.0.0.1", 9191

def main(nickname: str, message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(3)
        s.sendto(f"JOIN:{nickname}".encode(), (HOST, PORT))
        time.sleep(0.1)
        if message:
            s.sendto(f"MSG:{message}".encode(), (HOST, PORT))
            time.sleep(0.1)
        s.sendto(b"LEAVE", (HOST, PORT))
        print(f"[client] {nickname} done")

if __name__ == "__main__":
    nick = sys.argv[1] if len(sys.argv) > 1 else "Anon"
    msg  = sys.argv[2] if len(sys.argv) > 2 else ""
    main(nick, msg)
