# UserOrder API
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-red?logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-SimpleJWT-orange?logo=jsonwebtokens&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Engine-2496ED?logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker--Compose-1.29.2-003F8C?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-ReverseProxy-009639?logo=nginx&logoColor=white)
![DRF Spectacular](https://img.shields.io/badge/DRF_Spectacular-0.27.1-blue?logo=openapi-initiative&logoColor=white)

Это веб-сервис для управления пользователями и их заказами, построенный на Django и Django REST Framework. Проект предоставляет REST API с поддержкой JWT-аутентификации, расширенной фильтрацией, пагинацией и интуитивно понятной административной панелью. Поддерживаются базы данных PostgreSQL и SQLite, а развертывание упрощено благодаря Docker и Docker Compose.


### Основные возможности:
- Регистрация, аутентификация и авторизация пользователей
- JWT токены для безопасного доступа
- CRUD операции для пользователей и заказов
- API документация (Swagger UI и ReDoc)
- Административная панель с фильтрами, включая динамический, рассчитывающий диапазоны на основе данных
- Валидация данных
- Автоматическое вычисление возраста на основе даты рождения
- Пагинация результатов
- Расширенная фильтрация и поиск с разграничением прав для админов и обычных пользователей
   - Для пользователей: фильтрация по возрасту, диапазону возраста, дате рождения; поиск по username и email.
   - Для заказов: фильтрация по username, email, дате создания и обновления; поиск по названию и описанию.
   - Разграничение прав: администраторы видят все данные, обычные пользователи — только свои заказы.
- Поддержка PostgreSQL и SQLite

---

## Технический стек

- Python 3.10+
- Django 4.2.23
- Django REST Framework 3.16.0
- JWT (djangorestframework-simplejwt 5.5.0)
- PostgreSQL / SQLite
- Docker & Docker Compose
- DRF Spectacular

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
    - Запустить контенеры `docker compose up` (для запуска в фоне добавьте флаг`-d`)
    - Остановить контейнеры `docker compose down`
    - Перезапустить контенеры `docker compose restart` 
    - Пересобрать контейнеры `docker compose build`
    - Просмотр логов `docker compose logs -f`

---

## Загрузка тестовых данных
Для быстрого наполнения проекта начальными данными, для тестирования и демонстрации функциональности, можно загрузить заранее подготовленные фикстуры.

**Важно:** 
- В фикстурах пользоватеоя первичные ключи `(pk)` начинаются с `2`, чтобы избежать перезаписи суперпользователя, создаваемого вручную.
- У всех создаваемых пользователей задан пароль `TestPass`.
- <details>
  <summary>Список всех <code>username</code> из фикстуры (кликните, чтобы развернуть)</summary>
  <ul>
    <li>ivan_ivanov</li>
    <li>anna_smirnova</li>
    <li>dmitry_petrov</li>
    <li>ekaterina_kuznetsova</li>
    <li>alexey_morozov</li>
    <li>marina_volkova</li>
    <li>pavel_sokolov</li>
    <li>olga_novikova</li>
    <li>sergey_fedorov</li>
    <li>yulia_mikhailova</li>
    <li>vladimir_kovalev</li>
    <li>natalia_popova</li>
    <li>mikhail_egorov</li>
    <li>svetlana_ivanova</li>
    <li>andrey_smirnov</li>
    <li>elena_koroleva</li>
    <li>nikita_zaitsev</li>
    <li>tatiana_romanova</li>
    <li>roman_antonov</li>
    <li>kristina_orlova</li>
  </ul>
</details>

Находясь в корне проекта, выполните:

- Локальный запуск `python user_order_api/manage.py loaddata fixtures/data.json`
- В Docker-контейнере `docker compose exec backend python manage.py loaddata fixtures/data.json`

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
Проект предоставляет автоматически генерируемую документацию API через:

- **Swagger UI**: [`http://127.0.0.1:9000/api/docs/`](http://127.0.0.1:9000/api/docs/)
- **ReDoc**: [`http://127.0.0.1:9000/api/redoc/`](http://127.0.0.1:9000/api/redoc/)
- **JSON Schema**: [`http://127.0.0.1:9000/api/schema/`](http://127.0.0.1:9000/api/schema/)

### Основные эндпоинты API:

#### Аутентификация
- `POST /api/auth/signup/` - Регистрация нового пользователя
- `POST /api/auth/token/` - Получение JWT токена

#### Пользователи (для админов)
- `GET /api/users/` - Список пользователей
- `GET /api/users/{username}/` - Получение пользователя по username
- `PATCH /api/users/{username}/` - Частичное обновление пользователя
- `DELETE /api/users/{username}/` - Удаление пользователя

#### Профиль
- `GET /api/me/` - Получение данных текущего пользователя
- `PATCH /api/me/` - Обновление данных текущего пользователя
- `DELETE /api/me/` - Удаление текущего аккаунта

#### Заказы
- `GET /api/orders/` - Список заказов (только свои, для админов - все)
- `POST /api/orders/` - Создание нового заказа
- `GET /api/orders/{id}/` - Детали заказа
- `PATCH /api/orders/{id}/` - Обновление заказа
- `DELETE /api/orders/{id}/` - Удаление заказа
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
