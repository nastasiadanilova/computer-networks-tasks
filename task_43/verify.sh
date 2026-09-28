#!/bin/bash
pass() { echo "[✓] $1"; }
fail() { echo "[✗] $1"; exit 1; }

sleep 3  # wait for healthchecks

for svc in haproxy backend1 backend2 backend3; do
    docker inspect $svc > /dev/null 2>&1 && pass "$svc running" || fail "$svc not running"
done

# Round-robin check: 6 запросов → должны получить ответы от всех 3 бэкендов
BACKENDS=$(for i in $(seq 1 9); do
    curl -s http://127.0.0.1:8080/ | python3 -c "import sys,json; print(json.load(sys.stdin)['backend'])"
done | sort -u | wc -l)

[ "$BACKENDS" -ge 3 ] && pass "Round-robin: got responses from 3 different backends" || fail "Round-robin not working (only $BACKENDS backends responded)"

