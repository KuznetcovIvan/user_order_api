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

## Локальная установка и запуск без контейнеров с SQLite

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

7. Примените миграции:
   - Windows:
     `python user_order_api/manage.py migrate`
   - Linux/macOS:
     `python3 user_order_api/manage.py migrate`

8. Создайте суперпользователя:
  - Windows:
    `python user_order_api/manage.py createsuperuser`
  - Linux/macOS:
    `python3 user_order_api/manage.py createsuperuser`

9. Запустите приложение:
   - Windows:
     `python user_order_api/manage.py runserver`
   - Linux/macOS:
     `python3 user_order_api/manage.py runserver`

  - API будет доступен по адресу [`http://127.0.0.1:8000/api/`](http://127.0.0.1:8000/api/).
  - Административная панель по адресу [`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/).


## Установка и запуск в Docker Compose с PostgreSQL

1. Клонируйте проект с [репозитория](https://github.com/KuznetcovIvan/user_order_api):
   `https://github.com/KuznetcovIvan/user_order_api.git`

2. Перейдите в директорию с проектом:
   `cd user_order_api`

3. Создайте файл `.env` в корне проекта и задайте переменные окружения.
   Пример содержимого указан в файле [`.env.example`](./.env.example).

4. Находясь в корне проекта выполните команду `docker compose up -d`:
    - будут собраны образы
    - создадутся и запустятся контейнеры
    - настроятся тома и сеть согласно docker-compose.yml
    - сервисы запустятся в фоне (без вывода логов в терминал)
5. Находясь в корне проекта, зайдите в контенер с приложением и выполните миграции `docker compose exec backend python manage.py migrate`.
6. Соберите статические файлы приложения `docker compose exec backend python manage.py collectstatic`.
7. Скопируйте статические файлы в том `docker compose exec backend cp -r /app/collected_static/. /backend_static/static/`.
8. Создайте суперпользователя `docker compose exec backend python manage.py createsuperuser`.
  - API будет доступен по адресу [`http://127.0.0.1:9000/api/`](http://127.0.0.1:9000/api/).
  - Административная панель по адресу [`http://127.0.0.1:9000/admin/`](http://127.0.0.1:9000/admin/).
  - Управление контенерами:
    - Остановить контейнеры `docker compose down`
    - Перезапустить контенеры `docker compose restart`
    - Просмотр логов `docker compose logs -f`

---
## Возможные проблемы и пути решения
- Запуск приложения на занятом порту `Address already in use`:
   - В первом варианте запуска (запуск без контейнеров) укажите альтернативный свободный порт `python manage.py runserver 8080`
   - Во втором варианте (Docker Compose с PostgreSQL) внесите изменение в файле `docker-compose.yml` расположенном в корне проекта
   ```bash
   gateway:
    build: ./nginx/
    env_file: .env
    ports:
      - 9000:80  # Укажите вмето '9000' свободный порт.
    ...
   ```
- При изменении `.env` и повторных запусках в одном терминале переменные окружения могут не обновляться, так как загружаются только при первом запуске, что может вызвать ошибки из-за устаревших значений.
   - Запускайте каждую конфигурацию в отдельном окне терминала для загрузки актуальных переменных из `.env`.
   - Либо перед запуском явно перезагружайте `.env` командой `source .env`

---

## API Документация

---

## Административная панель

### Доступ к админке
URL: [`http://127.0.0.1:9000/admin/`](http://127.0.0.1:9000/admin/)

### Возможности админки

#### Управление пользователями
- **Список**: ID, логин, email, дата рождения, возраст, дата регистрации, количество заказов
- **Фильтры**: 
  - По возрастным группам (не задан, до 18, 18-25, 26-35, 36-50, 50+)
  - По количеству заказов (нет, мало, средне, много)
  - По дате регистрации
- **Поиск**: по email и username
- **Редактирование**: все поля пользователя кроме пароля

#### Управление заказами  
- **Список**: ID, название, описание, пользователь, дата создания, дата обновления
- **Фильтры**: по дате создания и обновления
- **Поиск**: по ID, названию, описанию, username пользователя
- **Только чтение**: поле пользователя

---

### Автор: [Иван Кузнецов](https://github.com/KuznetcovIvan)
