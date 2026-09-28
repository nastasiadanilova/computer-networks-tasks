#!/bin/bash
pass() { echo "[✓] $1"; }
fail() { echo "[✗] $1"; exit 1; }

docker inspect coredns > /dev/null 2>&1 && pass "CoreDNS running" || fail "CoreDNS not running"

IP=$(docker exec client dig +short web.lab.internal @172.20.0.53 2>/dev/null | head -1)
[ "$IP" = "172.20.0.10" ] && pass "DNS resolves web.lab.internal -> $IP" || fail "DNS failed: got '$IP'"

CODE=$(docker exec client curl -s -o /dev/null -w "%{http_code}" http://web.lab.internal 2>/dev/null)
[ "$CODE" = "200" ] && pass "HTTP request to web.lab.internal returns 200" || fail "HTTP failed: code $CODE"

