from app.core.security import SecurityService
from app.repositories.user import UserRepository
from app.repositories.token import TokenRepository
from app.models.user import User, UserLogin
from app.models.token import Token, RefreshTokenCreate


class AdminService:
    """Сервис аутентификации"""

    def __init__(
        self,
        user_repo: UserRepository,
        token_repo: TokenRepository,
        security_service: SecurityService = SecurityService
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.security_service = security_service

    async def get_users(self):
        return await self.user_repo.get_all_users()
