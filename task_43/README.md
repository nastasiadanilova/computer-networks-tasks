# Задание 43. HAProxy + 3 бэкенда (балансировка нагрузки)

## Условие

Развернуть кластер: HAProxy балансирует HTTP-запросы между тремя Python-бэкендами методом Round-Robin. Каждый бэкенд отвечает своим именем.
Файлы: docker-compose.yml, haproxy/haproxy.cfg, backend/app.py, verify.sh Проверка

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
