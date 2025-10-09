from typing import Optional
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

        await self.token_repo.create_refresh_token(token_data)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def login_user(self, user_data: UserLogin) -> Optional[User]:
        """Аутентификация пользователя"""
        user = await self.user_repo.get_user_by_email(user_data.email)
        if user and self.security_service.verify_password(user_data.password, user.password_hash):
            return user
        return None


    async def refresh_tokens(self, refresh_token: str) -> Optional[Token]:
        """Обновление токенов"""
        # Проверяем валидность токена
        payload = self.security_service.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        # Проверяем наличие токена в базе
        stored_token = await self.token_repo.get_refresh_token(refresh_token)
        if not stored_token:
            return None

        # Проверяем expiration
        if self.security_service.is_token_expired(stored_token.expires_at):
            await self.token_repo.delete_refresh_token(refresh_token)
            raise ValueError("Refresh token expired")

        # Получаем пользователя
        user_id = int(payload["sub"])
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            return None

        # Отзываем старый токен
        await self.token_repo.delete_refresh_token(refresh_token)

        # Создаем новые токены
        return await self.create_tokens(user)
    #
    # def logout(self, refresh_token: str) -> None:
    #     """Выход из системы"""
    #     self.token_repo.delete_refresh_token(refresh_token)
    #
    # def logout_all(self, user_id: int) -> None:
    #     """Выход из всех устройств"""
    #     self.token_repo.delete_user_refresh_tokens(user_id)
