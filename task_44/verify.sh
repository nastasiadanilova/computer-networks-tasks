#!/bin/bash
pass() { echo "[✓] $1"; }
fail() { echo "[✗] $1"; exit 1; }

docker inspect wg_a > /dev/null 2>&1 && pass "wg_a running" || fail "wg_a not running"
docker inspect wg_b > /dev/null 2>&1 && pass "wg_b running" || fail "wg_b not running"

docker exec wg_a wg show wg0 > /dev/null 2>&1 && pass "WireGuard interface up on wg_a" || fail "WireGuard down on wg_a"
docker exec wg_b wg show wg0 > /dev/null 2>&1 && pass "WireGuard interface up on wg_b" || fail "WireGuard down on wg_b"

docker exec host_a ping -c 3 -W 3 10.10.2.10 > /dev/null 2>&1 \
  && pass "host_a pings host_b through VPN tunnel" \
  || fail "host_a cannot ping host_b"

