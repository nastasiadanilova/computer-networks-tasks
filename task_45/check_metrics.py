#!/usr/bin/env python3
"""
Проверка доступности стека мониторинга.
Запуск: python3 check_metrics.py
"""
import urllib.request
import json
import sys

BASE_PROM = "http://127.0.0.1:9090"
BASE_GRAF = "http://127.0.0.1:3000"
BASE_ALRT = "http://127.0.0.1:9093"

errors = 0

def check(label: str, ok: bool, detail: str = ""):
    global errors
    if ok:
        print(f"[✓] {label}")
    else:
        print(f"[✗] {label}" + (f" ({detail})" if detail else ""))
        errors += 1

def http_get(url: str, timeout: int = 5):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, r.read().decode()
    except Exception as e:
        return None, str(e)

# 1. Prometheus
code, body = http_get(f"{BASE_PROM}/-/healthy")
check("Prometheus reachable", code == 200, f"HTTP {code}")

# 2. node_network метрики
code, body = http_get(f"{BASE_PROM}/api/v1/query?query=node_network_receive_bytes_total")
if code == 200:
    data = json.loads(body)
    has_metric = bool(data.get("data", {}).get("result"))
    check("node_network_receive_bytes_total metric exists", has_metric,
          "no data" if not has_metric else "")
else:
    check("node_network_receive_bytes_total metric exists", False, f"HTTP {code}")

code, body = http_get(f"{BASE_PROM}/api/v1/query?query=node_network_transmit_bytes_total")
if code == 200:
    data = json.loads(body)
    has_metric = bool(data.get("data", {}).get("result"))
    check("node_network_transmit_bytes_total metric exists", has_metric)
else:
    check("node_network_transmit_bytes_total metric exists", False, f"HTTP {code}")

# 3. Grafana
code, _ = http_get(f"{BASE_GRAF}/api/health")
check("Grafana reachable (HTTP 200)", code == 200, f"HTTP {code}")

# 4. Alertmanager
code, _ = http_get(f"{BASE_ALRT}/-/healthy")
check("Alertmanager reachable", code == 200, f"HTTP {code}")

print(f"\n{'All checks passed!' if errors == 0 else f'{errors} check(s) failed.'}")
sys.exit(0 if errors == 0 else 1)
