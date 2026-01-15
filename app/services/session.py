from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from user_agents import parse

from app.repositories import SessionRepository, TokenRepository
from app.schemas import LoginSessionCreate, LoginSessionUpdate

class SessionService:
    """Сервис сессий входа"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = SessionRepository(db)
        self.token_repo = TokenRepository(db)

    @staticmethod
    def parse_user_agent(user_agent_string: str) -> dict:
        """Парсит User-Agent строку"""
        if not user_agent_string:
            return {}

        ua = parse(user_agent_string)
        return {
            'browser': ua.browser.family,
            'os': ua.os.family,
            'device': ua.device.family,
            'device_type': 'mobile' if ua.is_mobile else 
                           'tablet' if ua.is_tablet else 
                           'desktop' if ua.is_pc else 
                           'unknown',
        }

    async def create_login_session(
        self,
        user_id: int,
        refresh_token: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> None:
        """Создает запись о новой сессии входа"""
        db_refresh_token = await self.token_repo.get_by_token(refresh_token)
        if not db_refresh_token:
            return

        session_info = {}
        if user_agent:
            parsed = SessionService.parse_user_agent(user_agent)
            session_info.update({
                'device_type': parsed.get('device_type'),
                'browser': parsed.get('browser'),
                'os': parsed.get('os'),
                'platform': parsed.get('os', '').split()[0] if parsed.get('os') else None
            })

        login_session = LoginSessionCreate(
            user_id=user_id,
            refresh_token_id=db_refresh_token.id,
            ip_address=ip_address,
            user_agent=user_agent,
            **session_info
        )
        await self.repo.create(login_session)
        await self.db.commit()

    async def update_login_session(
        self,
        refresh_token: str,
        ip_address: Optional[str] = None,
    ) -> None:
        """Обновить запись о сессии входа"""
        db_refresh_token = await self.token_repo.get_by_token(refresh_token)
        if not db_refresh_token:
            return

        db_login_session = await self.repo.get_by_token_id(db_refresh_token.id)

        login_session = LoginSessionUpdate(
            ip_address=ip_address,
            last_activity_at=datetime.now(timezone.utc)
        )
        await self.repo.update(db_login_session.id, login_session)
        await self.db.commit()
