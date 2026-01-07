from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import SecurityService
from app.repositories import UserRepository, TokenRepository
from app.schemas.user import User, UserCreate, UserLogin
from app.schemas.token import UserTokens, RefreshTokenCreate


class AuthService:
    """Сервис аутентификации"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)
        self.security_service = SecurityService

    async def register(self, user_data: UserLogin) -> User:
        """Регистрация нового пользователя"""
        # Проверка существования пользователя
        if await self.user_repo.get_by_email(user_data.email):
            raise ValueError('Пользователь с таким email уже существует')

        password_hash = self.security_service.get_password_hash(user_data.password)
        user_create = UserCreate(
            email=user_data.email,
            password_hash=password_hash
        )

        user = await self.user_repo.create(user_create)
        await self.db.commit()
        return user

    async def create_tokens(self, user: User) -> UserTokens:
        """Создание access и refresh токенов"""
        access_token = self.security_service.create_access_token(user)
        refresh_token = self.security_service.create_refresh_token(user)

        # Сохраняем refresh токен в базу
        refresh_payload = self.security_service.verify_token(refresh_token)
        if not refresh_payload:
            raise ValueError('Не удалось создать refresh token')

        token_data = RefreshTokenCreate(
            user_id=user.id,
            token=refresh_token,
            expires_at=refresh_payload['exp']
        )

        await self.token_repo.create(token_data)
        await self.user_repo.update_last_active(user.id)
        await self.db.commit()

        return UserTokens(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def login(self, user_data: UserLogin) -> Optional[User]:
        """Аутентификация пользователя"""
        user = await self.user_repo.get_by_email(user_data.email)
        if user and self.security_service.verify_password(user_data.password, user.password_hash):
            return user
        return None


    async def refresh_tokens(self, refresh_token: str) -> Optional[UserTokens]:
        """Обновление токенов"""
        # Проверяем валидность токена
        payload = self.security_service.verify_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return None

        # Проверяем наличие токена в базе
        stored_token = await self.token_repo.get_by_token(refresh_token)
        if not stored_token:
            return None

        # Проверяем expiration
        if self.security_service.is_token_expired(stored_token.expires_at):
            await self.token_repo.delete(stored_token.id)
            await self.db.commit()
            return None

        # Получаем пользователя
        user_id = int(payload['sub'])
        user = await self.user_repo.get(user_id)
        if not user:
            return None
        # self.token_repo.update_refresh_token(token_id, new_token, expires_at)

        # Удаляем старый токен
        await self.token_repo.delete(stored_token.id)
        await self.db.commit()

        # Создаем новые токены
        return await self.create_tokens(user)

    async def logout(self, refresh_token: str) -> None:
        """Выход из системы"""
        token = await self.token_repo.get_by_token(refresh_token)
        if token:
            await self.token_repo.delete(token.id)
            await self.db.commit()

    async def logout_all(self, user_id: int) -> None:
        """Выход из всех устройств"""
        await self.token_repo.delete_user_tokens(user_id)
        await self.db.commit()
