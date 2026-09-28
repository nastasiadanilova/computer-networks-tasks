from http.server import BaseHTTPRequestHandler, HTTPServer
import json, re

_store = {}
_counter = [0]

def json_resp(handler, code, data):
    body = json.dumps(data).encode()
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(body)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        if self.path == "/devices":
            json_resp(self, 200, list(_store.values()))
        elif m := re.match(r"^/devices/(\d+)$", self.path):
            did = int(m.group(1))
            if did in _store:
                json_resp(self, 200, _store[did])
            else:
                json_resp(self, 404, {"error": "not found"})
        else:
            json_resp(self, 404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/devices":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            _counter[0] += 1
            dev = {"id": _counter[0], "name": body.get("name",""),
                   "ip": body.get("ip",""), "type": body.get("type","unknown")}
            _store[_counter[0]] = dev
            json_resp(self, 201, dev)
        else:
            json_resp(self, 404, {"error": "not found"})

    def do_DELETE(self):
        if m := re.match(r"^/devices/(\d+)$", self.path):
            did = int(m.group(1))
            if did in _store:
                del _store[did]
                json_resp(self, 200, {"deleted": did})
            else:
                json_resp(self, 404, {"error": "not found"})
        else:
            json_resp(self, 404, {"error": "not found"})

if __name__ == "__main__":
    s = HTTPServer(("127.0.0.1", 8080), Handler)
    print("REST API running on 127.0.0.1:8080")
    s.serve_forever()
