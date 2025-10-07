from app.core.security import SecurityService
from app.repositories.user import UserRepository
from app.repositories.token import TokenRepository
from app.models.user import User, UserLogin
from app.models.token import Token, RefreshTokenCreate


class AuthService:
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

    async def register_user(self, user_data: UserLogin) -> User:
        """Регистрация нового пользователя"""
        # Проверка существования пользователя
        if await self.user_repo.get_user_by_email(user_data.email):
            raise ValueError("User with this email already exists")

        password_hash = self.security_service.get_password_hash(user_data.password)
        return await self.user_repo.create_user(user_data.email, password_hash)

    async def create_tokens(self, user: User) -> Token:
        """Создание access и refresh токенов"""
        access_token = self.security_service.create_access_token(user.id)
        refresh_token = self.security_service.create_refresh_token(user.id)

        # Сохраняем refresh токен в базу
        refresh_payload = self.security_service.verify_token(refresh_token)
        token_data = RefreshTokenCreate(
            user_id=user.id,
            token=refresh_token,
            expires_at=refresh_payload["exp"]
        )
        self.token_repo.create_refresh_token(token_data)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
