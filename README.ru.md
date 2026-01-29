# Auth Service API

[English](README.md) | [Русский](README.ru.md)

Микросервис аутентификации и управления пользователями на основе FastAPI с поддержкой JWT токенов, сессий и ролевой модели доступа.

## Технологический стек

- **Фреймворк**: FastAPI
- **База данных**: PostgreSQL
- **Асинхронность**: async/await, asyncpg
- **Аутентификация**: JWT (PyJWT), bcrypt
- **Миграции**: Alembic
- **Валидация**: Pydantic v2
- **Контейнеризация**: Docker, Docker Compose
- **Тестирование**: pytest, pytest-asyncio

## Основные возможности

- **Аутентификация**: Регистрация, вход, выход, обновление токенов
- **Безопасность**: JWT токены (access/refresh), хэширование паролей (bcrypt)
- **Управление пользователями**: CRUD операции, ролевая модель (USER, MODERATOR, ADMIN)
- **Мониторинг**: Трекинг сессий, активность пользователей, логирование входа
- **Производительность**: Асинхронная работа с БД, rate limiting
- **Тестирование**: Полный набор unit и интеграционных тестов


## Документация

- Swagger UI: `http://localhost:8000/auth/docs`
- ReDoc: `http://localhost:8000/auth/redoc`
- OpenAPI schema: `http://localhost:8000/auth/openapi.json`


## Быстрый старт

### Клонирование репозитория

```bash
git clone https://github.com/bro-Nik/portfolio-auth.git auth-service
cd auth-service
cp .env.example .env
# Отредактируйте .env файл
```
### Применение миграций
```bash
docker-compose exec auth alembic upgrade head
```
### Запуск приложения
```bash
docker-compose up
```
### Запуск тестов
```bash
docker-compose -f docker-compose.test.yml up
```
### Проверка работы
Откройте в браузере: `http://localhost:8000/auth/docs`


## API Endpoints

### Публичные (без аутентификации)
* `POST /register` - Регистрация нового пользователя

* `POST /login` - Вход в систему

* `POST /refresh` - Обновление токенов

### Пользовательские (требует access token)
* `DELETE /logout` - Выход из системы

* `DELETE /logout-all` - Выход со всех устройств

### Административные (требует роль ADMIN)
* `GET /admin/users` - Список пользователей

* `GET /admin/users/{id}` - Данные пользователя

* `POST /admin/users` - Создание пользователя

* `PUT /admin/users/{id}` - Обновление пользователя

* `DELETE /admin/users/{id}` - Удаление пользователя

* `DELETE /admin/users/{id}/logout-all` - Выход пользователя со всех устройств


## База данных

### Создать новую миграцию
```bash
docker-compose exec auth alembic revision -m "description"
```
### Применить миграции
```bash
docker-compose exec auth alembic upgrade head
```
### Откатить миграцию
```bash
docker-compose exec auth alembic downgrade -1
```
