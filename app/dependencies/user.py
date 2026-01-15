from app.dependencies.auth import get_current_user_role
from app.schemas.user import UserRole
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.services.user import UserService


async def get_user_service(
    db: AsyncSession = Depends(get_db),
    current_user_role: UserRole = Depends(get_current_user_role)
) -> UserService:
    """Зависимость для получения сервиса пользователей"""
    return UserService(db, current_user_role)
