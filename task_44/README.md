# Задание 44. VPN-туннель WireGuard между двумя сетями

## Условие

Смоделировать Site-to-Site VPN через WireGuard:
• Site A: сеть 10.10.1.0/24, шлюз wg_a (WireGuard endpoint :51820)
• Site B: сеть 10.10.2.0/24, шлюз wg_b (WireGuard endpoint :51821)
• VPN-туннель: 192.168.100.1 (wg_a) ↔ 192.168.100.2 (wg_b)
• host_a (10.10.1.10) должен доступен с host_b (10.10.2.10) через туннель
Файлы: docker-compose.yml, wg_a/wg0.conf, wg_b/wg0.conf, verify.sh

## Запуск

```bash
docker compose up -d
bash verify.sh
docker compose down
```

## Критерии



## Требования

- Docker Engine 24+
- Docker Compose v2
