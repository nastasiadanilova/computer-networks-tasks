# Задание 42. NS + Web-сервер в изолированной сети

## Условие

Развернуть в Docker Compose:
• Core DNS как внутренний DNS-сервер с зоной lab.internal
• Nginx web-сервер с именем web.lab.internal
• Клиентский контейнер client, разрешающий имена через Core DNS
Файлы: docker-compose.yml, coredns/Corefile, coredns/lab.internal.db, nginx/index.html, verify.sh Проверка

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
