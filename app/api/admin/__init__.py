from fastapi import APIRouter

from app.api.admin.endpoints import user


# Создание основного роутера
admin_router = APIRouter(prefix="/admin", tags=["admin"])


# Включение всех endpoints
admin_router.include_router(user.router)


# Экспорт
__all__ = ["admin_router"]
