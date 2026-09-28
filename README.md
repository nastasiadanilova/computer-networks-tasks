# Компьютерные сети - 50 практических заданий

Python 3.10+ | Docker Compose | НИУ ВШЭ

## Структура репозитория

| Папка | Задание | Тип |
|-------|---------|-----|
| `task_01/` | Перевод IP-адреса в двоичный формат | Python |
| `task_02/` | Определение класса IPv4-адреса | Python |
| `task_03/` | Калькулятор подсетей FLSM | Python |
| `task_04/` | VLSM: распределение адресного пространства | Python |
| `task_05/` | TCP echo-сервер и клиент | Python |
| `task_06/` | UDP-чат (клиент-сервер) | Python |
| `task_07/` | Многопоточный сканер портов | Python |
| `task_08/` | Симулятор таблицы ARP | Python |
| `task_09/` | Симулятор longest-prefix-match маршрутизации | Python |
| `task_10/` | HTTP REST API сервер (GET/POST/DELETE) | Python |
| `task_11/` | Симулятор DNS-резолвера с рекурсией и кешем | Python |
| `task_12/` | Калькулятор времени передачи и эффективности канала | Python |
| `task_13/` | Симулятор ACL (расширенный с логированием) | Python |
| `task_14/` | Симулятор DHCP-сервера | Python |
| `task_15/` | Симулятор NAT (Network Address Translation) | Python |
| `task_16/` | Анализатор лога сетевых пакетов | Python |
| `task_17/` | TCP-прокси (порт-форвардер) | Python |
| `task_18/` | Симулятор выборов Root Bridge (STP) | Python |
| `task_19/` | Симулятор VLAN-коммутатора | Python |
| `task_20/` | Парсер конфигурации Cisco IOS | Python |
| `task_21/` | Алгоритм Дейкстры для поиска кратчайшего пути в сети | Python |
| `task_22/` | Симулятор протокола скользящего окна (Go-Back-N) | Python |
| `task_23/` | Симулятор коллизий CSMA/CD | Python |
| `task_24/` | Симулятор Token Ring | Python |
| `task_25/` | Симулятор протокола RIP (дистанционно-векторная маршрутизация) | Python |
| `task_26/` | Генератор и валидатор MAC-адресов | Python |
| `task_27/` | Многопоточный HTTP-загрузчик с повторными попытками | Python |
| `task_28/` | Симулятор QoS-очередей (Priority Queue / WFQ) | Python |
| `task_41/` | Развертывание двухсегментной сети с маршрутизацией | Docker |
| `task_42/` | NS + Web-сервер в изолированной сети | Docker |
| `task_43/` | HAProxy + 3 бэкенда (балансировка нагрузки) | Docker |
| `task_44/` | VPN-туннель WireGuard между двумя сетями | Docker |
| `task_45/` | Полный стек мониторинга сети: Prometheus + Grafana + Node Exporter | Docker |

## Быстрый старт

### Python (задания 01-28)

```bash
git clone https://github.com/nastasiadanilova/computer-networks-tasks
cd computer-networks-tasks/task_01
python3 solution.py
```

### Docker (задания 41-45)

```bash
cd task_41
docker compose up -d
bash verify.sh
docker compose down
```

## Требования

- Python 3.10+
- Docker Engine 24+ и Docker Compose v2 (для заданий 41-45)
