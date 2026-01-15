from fastapi import APIRouter, Depends

from app.api.admin.endpoints import user
from app.dependencies import require_role
from app.schemas import UserRole


# Создание основного роутера
admin_router = APIRouter(
    prefix="/admin",
    tags="admin",
    dependencies=[Depends(require_role(UserRole.ADMIN))]
)


# Включение всех endpoints
admin_router.include_router(user.router)


# Экспорт
__all__ = ["admin_router"]
