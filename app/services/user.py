from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BusinessValidationError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
)
from app.core.security import SecurityService
from app.models import User
from app.repositories import UserRepository
from app.schemas.user import (
    UserCreateInternal,
    UserCreateRequest,
    UserRole,
    UserUpdateInternal,
    UserUpdateRequest,
)


class UserService:
    """Сервис для работы с пользователями."""

    def __init__(self, db: AsyncSession, current_user_role: UserRole):
        self.db = db
        self.repo = UserRepository(db)
        self.security_service = SecurityService()
        self.current_user_role = current_user_role

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Получение пользователя по ID."""
        return await self.repo.get(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        """Получение пользователя по email."""
        return await self.repo.get_by_email(email)

    async def get_user_with_details(self, user_id: int) -> User | None:
        """Получение пользователя по ID с детальной информацией."""
        return await self.repo.get_with_details(user_id)

    async def get_users_with_details(
        self,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
        role: str | None = None,
    ) -> list[User]:
        """Получение списка пользователей."""
        return await self.repo.get_all_with_details(skip, limit, search, role)

    async def create_user(self, user_data: UserCreateRequest) -> User:
        """Создать нового пользователя."""
        # Проверка прав
        self._check_create_permission()

        # Валидация
        await self._validate_create_data(user_data)

        user_to_db = UserCreateInternal(
            email=user_data.email,
            password_hash=self.security_service.get_password_hash(user_data.password),
            role=user_data.role,
            status=user_data.status,
        )

        # Создание
        async with self.db.begin():
            user = await self.repo.create(user_to_db)
            await self.db.refresh(user)
            return user

    async def update_user(self, user_id: int, user_data: UserUpdateRequest) -> User:
        """Обновить пользователя."""
        # Проверка прав
        self._check_update_permission()

        # Валидация
        await self._validate_update_data(user_id, user_data)

        user_internal = UserUpdateInternal(
            role=user_data.role,
            status=user_data.status,
        )

        # Обновление
        async with self.db.begin():
            user = await self.repo.update(user_id, user_internal)
            await self.db.refresh(user)
            return user

    async def delete_user(self, user_id: int) -> None:
        """Удалить пользователя."""
        # Проверка прав
        self._check_delete_permission()

        # Валидация
        await self._validate_delete_data(user_id)

        # Удаление
        async with self.db.begin():
            await self.repo.delete(user_id)

    def _check_create_permission(self) -> None:
        """Проверка прав на создание пользователя."""
        if self.current_user_role != UserRole.ADMIN:
            raise PermissionDeniedError(
                message='Только администраторы могут создавать пользователей',
            )

    def _check_update_permission(self) -> None:
        """Проверка прав на обновление пользователя."""
        if self.current_user_role != UserRole.ADMIN:
            raise PermissionDeniedError(
                message='Только администраторы могут изменять пользователей',
            )

    def _check_delete_permission(self) -> None:
        """Проверка прав на удаление пользователя."""
        if self.current_user_role != UserRole.ADMIN:
            raise PermissionDeniedError(
                message='Только администраторы могут удалять пользователей',
            )

    async def _validate_create_data(self, data: UserCreateRequest) -> None:
        """Валидация данных для создания пользователя."""
        # Проверка иерархии ролей
        if data.role.priority >= self.current_user_role.priority:
            raise BusinessValidationError(
                message='Нельзя назначать права, равные или превышающие ваши',
            )

        # Проверка уникальности email
        existing = await self.get_user_by_email(data.email)
        if existing:
            raise ConflictError(
                message=f'Пользователь с email {data.email} уже существует',
            )

    async def _validate_update_data(self, user_id:int, data: UserUpdateRequest) -> None:
        """Валидация данных для обновления пользователя."""
        # Проверка иерархии ролей
        if data.role and data.role.priority >= self.current_user_role.priority:
            raise BusinessValidationError(
                message='Нельзя назначать права, равные или превышающие ваши',
            )

        # Проверка существования пользователя
        user = await self.repo.get(user_id)
        if not user:
            raise NotFoundError(message='Пользователь не найден')

    async def _validate_delete_data(self, user_id:int) -> None:
        """Валидация данных для удаления пользователя."""
        # Проверка существования пользователя
        user_to_delete = await self.repo.get(user_id)
        if not user_to_delete:
            raise NotFoundError(message='Пользователь не найден')

        # Можно удалить только пользователя с меньшей ролью
        if user_to_delete.role.priority >= self.current_user_role.priority:
            raise BusinessValidationError(
                message='Нельзя удалить пользователя с ролью, равной или выше вашей',
            )
