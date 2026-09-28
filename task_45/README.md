# Задание 45. Полный стек мониторинга сети: Prometheus + Grafana + Node Exporter

## Условие

Развернуть стек мониторинга сетевых метрик:
• Prometheus - сбор метрик (порт 9090)
• Node Exporter - метрики хоста: сетевые интерфейсы, пакеты, байты
• Grafana - визуализация (порт 3000, login: admin/admin)
• Alertmanager - алерты (порт 9093)
• Python-скрипт check_metrics.py - проверяет наличие метрик node_network_*Файлы: docker-compose.yml, prometheus/prometheus.yml, prometheus/alert.rules.yml, grafana/dashboards/network.json, check_metrics.py

## Запуск

```bash
docker compose up -d
bash verify.sh
docker compose down
```

## Критерии

- • Все 4 сервиса запущены и доступны по портам
- • Prometheus успешно скрапит node_exporter (status=up в targets)
- • check_metrics.py возвращает 0 ошибок

## Требования

- Docker Engine 24+
- Docker Compose v2
