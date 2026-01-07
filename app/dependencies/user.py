from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.services.user import UserService


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Зависимость для получения сервиса пользователей"""
    return UserService(db)
