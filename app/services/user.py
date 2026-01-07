from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories import UserRepository


class UserService:
    """Сервис для работы с пользователями"""

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        user = await self.repo.get(user_id)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        user = await self.repo.get_by_email(email)
        return user

    async def get_users(self) -> List[User]:
        """Получение списка пользователей"""
        users = await self.repo.get_all()
        return users
