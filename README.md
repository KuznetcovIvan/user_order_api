# UserOrder API
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red?logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-SimpleJWT-orange?logo=jsonwebtokens&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Engine-2496ED?logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker--Compose-1.29.2-003F8C?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-ReverseProxy-009639?logo=nginx&logoColor=white)

Это веб-сервис для управления пользователями и их заказами. Проект предоставляет полнофункциональный API с аутентификацией, авторизацией и административным интерфейсом.


### Основные возможности:
- Регистрация, аутентификация и авторизация пользователей
- JWT токены для безопасного доступа
- CRUD операции для пользователей и заказов
- Административная панель с фильтрами, включая динамический, рассчитывающий диапазоны на основе данных
- Валидация данных
- Автоматическое вычисление возраста на основе даты рождения
- Пагинация результатов
- Поддержка PostgreSQL и SQLite

---

## Технический стек

- Django 4.2.23
- Django REST Framework 3.16.0
- JWT (djangorestframework-simplejwt 5.5.0)
- PostgreSQL / SQLite
- Docker & Docker Compose

---

## Локальная установка и запуск (SQLite)

1. Клонируйте проект с [репозитория](https://github.com/KuznetcovIvan/user_order_api):
   `https://github.com/KuznetcovIvan/user_order_api.git`

2. Перейдите в директорию с проектом:
   `cd user_order_api`

3. Создайте виртуальное окружение в директории проекта:  
   - Windows: `python -m venv venv`  
   - Linux/macOS: `python3 -m venv venv`

4. Активируйте виртуальное окружение:  
   - Windows: `source venv/Scripts/activate`  
   - Linux/macOS: `source venv/bin/activate`

5. Установите зависимости:
   `pip install -r user_order_api/requirements.txt`

6. Создайте файл `.env` в корне проекта и задайте переменные окружения.
   Пример содержимого указан в файле [`.env.example`](./.env.example).

7. Примените миграции `alembic upgrade head`.

8. Запустите приложение `uvicorn app.main:app`

  - Приложение запустится на [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
  - При первом запуске приложения, при наличии в файле `.env` переменных `FIRST_SUPERUSER_EMAIL` и `FIRST_SUPERUSER_PASSWORD`, будет создан суперпользователь с соответствующим `EMAIL` и `PASSWORD`.


Содержимое `.env`:
```env
# Django настройки
SECRET_KEY=your_very_secret_key_here_change_this_in_production
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1

# База данных (для PostgreSQL)
DB_TYPE=postgres
POSTGRES_DB=userorder_db
POSTGRES_USER=userorder_user
POSTGRES_PASSWORD=userorder_password
DB_HOST=localhost
DB_PORT=5432

# Для SQLite (по умолчанию)
# DB_TYPE=sqlite

# Дополнительные настройки
PASSWORD_MIN_LENGTH=8
PROFILE_URL_SEGMENT=me
```

5. **Применение миграций**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Создание суперпользователя**
```bash
python manage.py createsuperuser
```

7. **Запуск сервера разработки**
```bash
python manage.py runserver
```

API будет доступен по адресу: `http://127.0.0.1:8000/api/`

## 🐳 Docker развертывание

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание непривилегированного пользователя
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Экспорт порта
EXPOSE 8000

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: userorder_postgres
    environment:
      POSTGRES_DB: userorder_db
      POSTGRES_USER: userorder_user
      POSTGRES_PASSWORD: userorder_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U userorder_user -d userorder_db"]
      interval: 30s
      timeout: 10s
      retries: 3

  web:
    build: .
    container_name: userorder_api
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    environment:
      - DB_TYPE=postgres
      - POSTGRES_DB=userorder_db
      - POSTGRES_USER=userorder_user
      - POSTGRES_PASSWORD=userorder_password
      - DB_HOST=db
      - DB_PORT=5432
      - DEBUG=False
      - ALLOWED_HOSTS=localhost 127.0.0.1
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: userorder_nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
```

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream web {
        server web:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location /static/ {
            alias /app/staticfiles/;
        }

        location / {
            proxy_pass http://web;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Запуск с Docker

```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Остановка сервисов
docker-compose down

# Остановка с удалением volumes
docker-compose down -v
```

### Управление контейнерами

```bash
# Выполнение команд в контейнере
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Подключение к базе данных
docker-compose exec db psql -U userorder_user -d userorder_db

# Просмотр работающих контейнеров
docker-compose ps

# Перезапуск конкретного сервиса
docker-compose restart web
```

## ⚙️ Конфигурация

### Основные настройки (settings.py)

```python
# Основные параметры проекта
PROJECT_NAME = 'UserOrder'
PASSWORD_MIN_LENGTH = 8
PROFILE_URL_SEGMENT = 'me'  # URL для профиля пользователя

# JWT настройки
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# DRF настройки
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

### Переменные окружения

| Переменная | Описание | По умолчанию | Обязательная |
|------------|----------|--------------|--------------|
| `SECRET_KEY` | Django секретный ключ | insecure_default_key... | Да |
| `DEBUG` | Режим отладки | False | Нет |
| `ALLOWED_HOSTS` | Разрешенные хосты | localhost 127.0.0.1 | Нет |
| `DB_TYPE` | Тип БД (sqlite/postgres) | sqlite | Нет |
| `POSTGRES_DB` | Имя базы PostgreSQL | django | Нет |
| `POSTGRES_USER` | Пользователь PostgreSQL | django | Нет |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | | Да (для PostgreSQL) |
| `DB_HOST` | Хост базы данных | | Да (для PostgreSQL) |
| `DB_PORT` | Порт базы данных | 5432 | Нет |

## 📖 API Документация

### Базовый URL: `http://127.0.0.1:8000/api/`

### Аутентификация (`/auth/`)

#### 🔐 Регистрация пользователя
```http
POST /api/auth/signup/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com", 
    "password": "securepassword123",
    "birth_date": "1990-01-15"
}
```

**Ответ 201:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "birth_date": "1990-01-15"
}
```

#### 🎫 Получение токена
```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepassword123"
}
```

**Ответ 200:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Пользователи (`/users/`)

#### 👥 Список пользователей (только админы)
```http
GET /api/users/
Authorization: Bearer <token>
```

**Ответ 200:**
```json
{
    "count": 25,
    "next": "http://127.0.0.1:8000/api/users/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "birth_date": "1990-01-15",
            "age": 34
        }
    ]
}
```

#### 👤 Текущий пользователь
```http
GET /api/users/me/
Authorization: Bearer <token>
```

**Ответ 200:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "birth_date": "1990-01-15"
}
```

#### ✏️ Обновление профиля
```http
PATCH /api/users/me/
Authorization: Bearer <token>
Content-Type: application/json

{
    "email": "newemail@example.com",
    "birth_date": "1990-01-20"
}
```

#### 👤 Получение пользователя по username (только админы)
```http
GET /api/users/{username}/
Authorization: Bearer <token>
```

### Заказы (`/orders/`)

#### 📦 Список заказов
```http
GET /api/orders/
Authorization: Bearer <token>
```

**Ответ для обычного пользователя:**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Заказ на разработку сайта",
            "description": "Нужен современный сайт для компании",
            "created_at": "2024-06-26T10:00:00Z"
        }
    ]
}
```

**Ответ для администратора:**
```json
{
    "count": 50,
    "next": "http://127.0.0.1:8000/api/orders/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Заказ на разработку сайта",
            "description": "Нужен современный сайт для компании",
            "created_at": "2024-06-26T10:00:00Z",
            "updated_at": "2024-06-26T10:00:00Z",
            "user": "john_doe"
        }
    ]
}
```

#### 📝 Создание заказа
```http
POST /api/orders/
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "Новый заказ",
    "description": "Подробное описание заказа"
}
```

#### 📖 Получение заказа
```http
GET /api/orders/{id}/
Authorization: Bearer <token>
```

#### ✏️ Обновление заказа
```http
PATCH /api/orders/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "Обновленное название",
    "description": "Обновленное описание"
}
```

#### 🗑️ Удаление заказа
```http
DELETE /api/orders/{id}/
Authorization: Bearer <token>
```

#### 👤 Заказы пользователя (только админы)
```http
GET /api/orders/{username}/
Authorization: Bearer <token>
```

### Коды ответов

| Код | Описание |
|-----|----------|
| 200 | Успешно |
| 201 | Создано |
| 204 | Удалено |
| 400 | Ошибка валидации |  
| 401 | Не авторизован |
| 403 | Доступ запрещен |
| 404 | Не найдено |
| 500 | Ошибка сервера |

## 🛡️ Админ-панель

### Доступ к админке
URL: `http://127.0.0.1:8000/admin/`

### Возможности админки

#### 👥 Управление пользователями
- **Список**: ID, логин, email, дата рождения, возраст, дата регистрации, количество заказов
- **Фильтры**: 
  - По возрастным группам (не задан, до 18, 18-25, 26-35, 36-50, 50+)
  - По количеству заказов (нет, мало, средне, много)
  - По дате регистрации
- **Поиск**: по email и username
- **Редактирование**: все поля пользователя кроме пароля

#### 📦 Управление заказами  
- **Список**: ID, название, описание, пользователь, дата создания, дата обновления
- **Фильтры**: по дате создания и обновления
- **Поиск**: по ID, названию, описанию, username пользователя
- **Только чтение**: поле пользователя

#### 🎨 Кастомизация
- Русифицированный интерфейс
- Кастомные заголовки страниц
- Автоматическое вычисление возраста
- Динамические фильтры по количеству заказов

### Создание суперпользователя
```bash
python manage.py createsuperuser
```

## 🗄️ База данных

### ERD диаграмма

```
┌─────────────────────────┐       ┌─────────────────────────┐
│        User             │       │        Order            │
├─────────────────────────┤       ├─────────────────────────┤
│ id (PK)                 │       │ id (PK)                 │
│ username (UNIQUE)       │       │ title                   │
│ email (UNIQUE)          │       │ description             │
│ birth_date (NULL)       │       │ user_id (FK)            │
│ password                │       │ created_at              │
│ is_staff                │       │ updated_at              │
│ is_active               │◄──────┤                         │
│ date_joined             │  1:N  │                         │
│ last_login              │       │                         │
└─────────────────────────┘       └─────────────────────────┘
```

### Настройка PostgreSQL

1. **Установка PostgreSQL**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Скачайте с официального сайта
```

2. **Создание базы данных**
```sql
CREATE DATABASE userorder_db;
CREATE USER userorder_user WITH PASSWORD 'userorder_password';
GRANT ALL PRIVILEGES ON DATABASE userorder_db TO userorder_user;
```

3. **Настройка .env**
```env
DB_TYPE=postgres
POSTGRES_DB=userorder_db
POSTGRES_USER=userorder_user
POSTGRES_PASSWORD=userorder_password
DB_HOST=localhost
DB_PORT=5432
```

### Миграции

```bash
# Создание новых миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Просмотр статуса миграций
python manage.py showmigrations

# Откат миграций
python manage.py migrate orders 0001

# Удаление всех данных
python manage.py flush
```

## 📊 Модели данных

### User (Пользователь)
```python
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Вычисляемые поля
    @property
    def age(self):
        # Автоматическое вычисление возраста
```

**Ограничения:**
- `username`: уникальный, до 150 символов, только буквы, цифры и @/./+/-/_
- `email`: уникальный, валидный email
- `birth_date`: не может быть в будущем, возраст не более 120 лет
- `username` не может быть равен значению `PROFILE_URL_SEGMENT` ("me")

### Order (Заказ)
```python
class Order(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Ограничения:**
- `title`: до 200 символов
- `description`: до 2000 символов
- `user`: связь с пользователем, каскадное удаление

## 🔐 Аутентификация

### JWT токены
Проект использует JWT (JSON Web Tokens) для аутентификации:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Получение токена
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'
```

### Использование токена
```bash
curl -H "Authorization: Bearer <your_token>" \
  http://127.0.0.1:8000/api/users/me/
```

### Время жизни токена
- **Access token**: 24 часа
- **Refresh token**: не используется (отключен)

## 🛡️ Права доступа

### Система разрешений

#### AllowAny
- `POST /api/auth/signup/` - регистрация
- `POST /api/auth/token/` - получение токена

#### IsAuthenticated
- `GET /api/users/me/` - профиль пользователя
- `PATCH /api/users/me/` - обновление профиля
- Все операции с заказами

#### IsAdminUser
- `GET /api/users/` - список пользователей
- `POST /api/users/` - создание пользователя
- `GET /api/users/{username}/` - получение пользователя
- `PATCH /api/users/{username}/` - обновление пользователя
- `DELETE /api/users/{username}/` - удаление пользователя
- `GET /api/orders/{username}/` - заказы пользователя

#### IsOrdererOrAdmin (кастомное разрешение)
- Пользователь может управлять только своими заказами
- Администратор может управлять всеми заказами

```python
class IsOrdererOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user
```

### Уровни доступа

| Роль | Пользователи | Заказы |
|------|-------------|--------|
| **Анонимный** | Регистрация, авторизация | - |
| **Пользователь** | Свой профиль | Свои заказы |
| **Администратор** | Все пользователи | Все заказы |

## 🧪 Тестирование API

### Ручное тестирование

#### 1. Регистрация пользователя
```bash
curl -X POST http://127.0.0.1:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "birth_date": "1990-01-01"
  }'
```

#### 2. Получение токена
```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access'])")
```

#### 3. Создание заказа
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Тестовый заказ",
    "description": "Описание тестового заказа"
  }'
```

#### 4. Получение списка заказов
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/orders/
```

### Postman коллекция

Создайте коллекцию в Postman с следующими запросами:

1. **Auth - Signup**
   - Method: POST
   - URL: `{{base_url}}/api/auth/signup/`
   - Body: JSON с данными пользователя

2. **Auth - Token**
   - Method: POST
   - URL: `{{base_url}}/api/auth/token/`
   - Body: JSON с username/password
   - Tests: Сохранение токена в переменную

3. **Users - Profile**
   - Method: GET
   - URL: `{{base_url}}/api/users/me/`
   - Headers: Authorization Bearer {{token}}

4. **Orders - List**
   - Method: GET
   - URL: `{{base_url}}/api/orders/`
   - Headers: Authorization Bearer {{token}}

5. **Orders - Create**
   - Method: POST
   - URL: `{{base_url}}/api/orders/`
   - Headers: Authorization Bearer {{token}}
   - Body: JSON с данными заказа

### Переменные Postman
```json
{
  "base_url": "http://127.0.0.1:8000",
  "token": "{{access_token}}"
}
```

## 💡 Примеры использования

### Python клиент

```python
import requests
import json

class UserOrderClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token = None
    
    def signup(self, username, email, password, birth_date=None):
        """Регистрация нового пользователя"""
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        if birth_date:
            data["birth_date"] = birth_date
            
        response = requests.post(f"{self.base_url}/api/auth/signup/", json=data)
        return response.json()
    
    def login(self, username, password):
        """Авторизация и получение токена"""
        data = {"username": username, "password": password}
        response = requests.post(f"{self.base_url}/api/auth/token/", json=data)
        if response.status_code == 200:
            self.token = response.json()["access"]
        return response.json()
    
    def get_headers(self):
        """Получение заголовков с токеном"""
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}
    
    def get_profile(self):
        """Получение профиля пользователя"""
        response = requests.get(
            f"{self.base_url}/api/users/me/", 
            headers=self.get_headers()
        )
        return response.json()
    
    def create_order(self, title, description):
        """Создание нового заказа"""
        data = {"title": title, "description": description}
        response = requests.post(
            f"{self.base_url}/api/orders/",
            json=data,
            headers=self.get_headers()
        )
        return response.json()
    
    def get_orders(self):
        """Получение списка заказов"""
        response = requests.get(
            f"{self.base_url}/api/orders/",
            headers=self.get_headers()
        )
        return response.json()

# Пример использования
client = UserOrderClient()

# Регистрация
client.signup("john_doe", "john@example.com", "securepass123", "1990-01-15")

# Авторизация
client.login("john_doe", "securepass123")

# Создание заказа
order = client.create_order("Разработка сайта", "Нужен современный сайт")
print(f"Создан заказ: {order}")

# Получение заказов
orders = client.get_orders()
print(f"Всего заказов: {orders['count']}")
```

### JavaScript клиент

```javascript
class UserOrderAPI {
    constructor(baseUrl = 'http://127.0.0.1:8000') {
        this.baseUrl = baseUrl;
        this.token = localStorage.getItem('access_token');
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        if (this.token) {
            config.headers.Authorization = `Bearer ${this.token}`;
        }
        
        const response = await fetch(url, config);
        return response.json();
    }
    
    async signup(userData) {
        return this.request('/api/auth/signup/', {