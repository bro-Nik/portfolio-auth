from typing import Optional

from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RefreshToken
from app.schemas import RefreshTokenCreate, RefreshTokenUpdate
from app.repositories.base import BaseRepository


class TokenRepository(BaseRepository[RefreshToken, RefreshTokenCreate, RefreshTokenUpdate]):
    """Репозиторий для работы с Refresh токенами"""
    def __init__(self, db: AsyncSession):
        super().__init__(RefreshToken, db)

    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        """Найти refresh токен в БД по его строковому значению"""
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.token == token))
        return result.scalar_one_or_none()

    async def delete_user_tokens(self, user_id: int) -> None:
        """Удалить все refresh токены пользователя"""
        result = await self.db.execute(select(RefreshToken).where(RefreshToken.user_id == user_id))
        tokens = result.scalars().all()
        for token in tokens:
            self.db.delete(token)
