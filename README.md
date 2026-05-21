# Lab 6 — DevOps, CI/CD, Docker

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/lab6/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/lab6/actions/workflows/ci.yml)

Простий REST API на Flask + PostgreSQL, контейнеризований через Docker, з повним CI/CD конвеєром на GitHub Actions.

---

## Зміст
- [Запуск через Docker](#запуск-через-docker)
- [Локальний запуск](#локальний-запуск)
- [Змінні середовища](#змінні-середовища)
- [API Endpoints](#api-endpoints)
- [Тести](#тести)
- [Як перевірити результат](#як-перевірити-результат)

---

## Запуск через Docker

### Передумови
- Docker Desktop ≥ 24.x
- Docker Compose ≥ 2.x

### Кроки

```bash
# 1. Клонуй репозиторій
git clone https://github.com/YOUR_USERNAME/lab6.git
cd lab6

# 2. Скопіюй файл змінних середовища
cp .env.example .env

# 3. Запусти всі сервіси (app + db)
docker compose up --build

# 4. Зупинити
docker compose down

# 5. Зупинити та видалити volumes (БД)
docker compose down -v
```

Додаток буде доступний на: **http://localhost:5000**

### Запуск тестів у Docker

```bash
docker compose --profile test up tests --build
```

---

## Локальний запуск

```bash
# 1. Створи віртуальне середовище
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows

# 2. Встанови залежності
pip install -r requirements.txt

# 3. Запусти PostgreSQL локально або через Docker
docker run -d --name pg \
  -e POSTGRES_DB=labdb \
  -e POSTGRES_USER=labuser \
  -e POSTGRES_PASSWORD=labpass \
  -p 5432:5432 postgres:16-alpine

# 4. Встанови змінні середовища
export DB_HOST=localhost DB_NAME=labdb DB_USER=labuser DB_PASSWORD=labpass

# 5. Запусти сервер
python app/app.py
```

---

## Змінні середовища

| Змінна | Опис | Значення за замовч. |
|---|---|---|
| `DB_HOST` | Хост PostgreSQL | `db` (Docker) / `localhost` |
| `DB_NAME` | Назва бази даних | `labdb` |
| `DB_USER` | Ім'я користувача БД | `labuser` |
| `DB_PASSWORD` | Пароль до БД | `labpass` |
| `APP_PORT` | Порт додатку | `5000` |
| `FLASK_ENV` | Режим Flask | `production` |

---

## API Endpoints

| Метод | URL | Опис | Тіло запиту |
|---|---|---|---|
| `GET` | `/` | Статус додатку | — |
| `GET` | `/health` | Health check | — |
| `GET` | `/items` | Список усіх елементів | — |
| `POST` | `/items` | Створити новий елемент | `{"name": "string"}` |

### Приклади запитів

```bash
# Перевірити статус
curl http://localhost:5000/

# Отримати всі елементи
curl http://localhost:5000/items

# Створити елемент
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "My Item"}'
```

---

## Тести

```bash
# Запустити всі тести
pytest tests/ -v

# З покриттям коду
pytest tests/ -v --cov=app --cov-report=term-missing

# У Docker
docker compose --profile test up tests --build
```

### Що тестується

| Тест | Опис |
|---|---|
| `test_index` | GET `/` повертає 200 і статус "ok" |
| `test_health` | GET `/health` повертає "healthy" |
| `test_create_item_missing_name` | POST без name повертає 400 |
| `test_get_items` | GET `/items` повертає список |
| `test_create_item` | POST `/items` створює елемент, повертає 201 |


## Структура проєкту

```
lab6/
├── app/
│   └── app.py              # Flask додаток
├── tests/
│   └── test_app.py         # Юніт-тести
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD
├── Dockerfile              # Образ продакшн
├── Dockerfile.test         # Образ для тестів
├── docker-compose.yaml     # Оркестрація сервісів
├── init.sql                # Ініціалізація БД
├── requirements.txt        # Python залежності
├── .env.example            # Шаблон змінних середовища
└── README.md
```
