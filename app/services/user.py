from typing import Optional
from app.repositories.user import UserRepository
from app.models.user import User

class UserService:
    """Сервис для работы с пользователями"""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        user = await self.user_repo.get_user_by_id(user_id)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Получение пользователя по email"""
        user = await self.user_repo.get_user_by_email(email)
        return user
