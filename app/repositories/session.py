from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import LoginSession
from app.schemas import LoginSessionCreate, LoginSessionUpdate
from app.repositories.base import BaseRepository


class SessionRepository(BaseRepository[LoginSession, LoginSessionCreate, LoginSessionUpdate]):
    """Репозиторий для работы с сессиями входа пользователя"""

    def __init__(self, db: AsyncSession):
        super().__init__(LoginSession, db)

    async def get_by_token_id(self, token_id: int) -> LoginSession:
        result = await self.db.execute(
            select(LoginSession).where(LoginSession.refresh_token_id == token_id)
        )
        return result.scalar_one_or_none()
