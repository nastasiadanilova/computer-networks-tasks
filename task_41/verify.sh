#!/bin/bash
set -e
pass() { echo "[✓] $1"; }
fail() { echo "[✗] $1"; exit 1; }

docker inspect router > /dev/null 2>&1 && pass "Router running" || fail "Router not running"
docker exec host_a ping -c 2 -W 2 10.0.2.10 > /dev/null 2>&1 && pass "host_a can ping host_b via router" || fail "host_a cannot ping host_b"
docker exec host_b ping -c 2 -W 2 10.0.1.10 > /dev/null 2>&1 && pass "host_b can ping host_a via router" || fail "host_b cannot ping host_a"

