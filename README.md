# Auth Service API

[English](README.md) | [Русский](README.ru.md)

A microservice for authentication and user management built on FastAPI with support for JWT tokens, sessions, and a role-based access model.

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Asynchronous**: async/await, asyncpg
- **Authentication**: JWT (PyJWT), bcrypt
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, pytest-asyncio

## Core Features

- **Authentication**: Registration, login, logout, token refresh
- **Security**: JWT tokens (access/refresh), password hashing (bcrypt)
- **User Management**: CRUD operations, role-based model (USER, MODERATOR, ADMIN)
- **Monitoring**: Session tracking, user activity, login logging
- **Performance**: Asynchronous database operations, rate limiting
- **Testing**: Comprehensive unit and integration tests


## Documentation

- Swagger UI: `http://localhost:8000/auth/docs`
- ReDoc: `http://localhost:8000/auth/redoc`
- OpenAPI schema: `http://localhost:8000/auth/openapi.json`


## Quick Start

### Clone the Repository

```bash
git clone https://github.com/bro-Nik/portfolio-auth.git auth-service
cd auth-service
cp .env.example .env
# Edit the .env file
```
### Apply Migrations
```bash
docker-compose exec auth alembic upgrade head
```
### Run the Application
```bash
docker-compose up
```
### Run Tests
```bash
docker-compose -f docker-compose.test.yml up
```
### Verify Operation
Open in your browser: `http://localhost:8000/auth/docs`


## API Endpoints

### Public (No Authentication Required)
* `POST /register` - Register a new user

* `POST /login` - Login to the system

* `POST /refresh` - Refresh tokens

### User (Requires Access Token)
* `DELETE /logout` - Logout from the system

* `DELETE /logout-all` - Logout from all devices

### Administrative (Requires ADMIN Role)
* `GET /admin/users` - List users

* `GET /admin/users/{id}` - Get user data

* `POST /admin/users` - Create a user

* `PUT /admin/users/{id}` - Update a user

* `DELETE /admin/users/{id}` - Delete a user

* `DELETE /admin/users/{id}/logout-all` - Logout a user from all devices


## Database

### Create a New Migration
```bash
docker-compose exec auth alembic revision -m "description"
```
### Apply Migrations
```bash
docker-compose exec auth alembic upgrade head
```
### Rollback a Migration
```bash
docker-compose exec auth alembic downgrade -1
```
