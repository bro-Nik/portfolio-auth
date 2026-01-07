from fastapi import APIRouter

from app.api.user.endpoints import auth


# Создание основного роутера
# user_router = APIRouter(prefix="/api", tags=["user"])
user_router = APIRouter()


# Включение всех endpoints
user_router.include_router(auth.router)


# Экспорт
__all__ = ["user_router"]
