from typing import List, Optional
from datetime import datetime, timezone

from app.schemas.user import UserCreateInternal, UserUpdateInternal
from sqlalchemy import select 
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreateInternal, UserUpdateInternal]):
    """Репозиторий для работы с пользователями"""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Найти пользователя по email"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update_activity(self, user_id) -> None:
        """Обновить метрики активности пользователя"""
        user = await self.get(user_id)
        if user:
            user.last_active_at = datetime.now(timezone.utc)
            user.total_active_time += settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    async def get_with_details(self, user_id: int) -> Optional[User]:
        """Получить пользователя с деталями"""
        query = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.login_sessions))
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_with_details(
        self,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        role: Optional[str] = None
    ) -> List[User]:
        """Получить список пользователей с пагинацией и деталями"""
        query = select(User).options(joinedload(User.login_sessions))

        # Применяем фильтры
        if search:
            # Ищем по email
            search_filter = User.email.ilike(f'%{search}%')
            query = query.where(search_filter)

        if role:
            query = query.where(User.role == role)

        # Применяем пагинацию
        query = query.offset(skip)
        if limit:
            query = query.limit(limit)

        # Сортируем
        query = query.order_by(User.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().unique().all()
