from typing import Optional
from datetime import datetime, timezone

from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Репозиторий для работы с пользователями"""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Найти пользователя по email"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update_last_active(self, user_id) -> None:
        """Обновить время последней активности пользователя"""
        user = await self.get(user_id)
        if user:
            user.last_active_at = datetime.now(timezone.utc).replace(tzinfo=None)
