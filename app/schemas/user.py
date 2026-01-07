from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    """Роли пользователей в системе"""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    @property
    def priority(self) -> int:
        """Приоритет роли для проверки прав (чем выше число, тем выше приоритет)"""
        priorities = {
            UserRole.USER: 1,
            UserRole.MODERATOR: 2,
            UserRole.ADMIN: 3,
        }
        return priorities.get(self, 1)


class User(BaseModel):
    """Модель пользователя для внутреннего использования"""
    id: int
    email: EmailStr
    password_hash: str | None = None
    role: UserRole = UserRole.USER


class UserCreate(BaseModel):
    """Схема для создания нового пользователя"""
    email: EmailStr
    password_hash: str  # Захэшированный пароль


class UserUpdate(BaseModel):
    """Схема для обновления данных пользователя"""
    id: int
    email: EmailStr
    password: str  # Пароль в открытом виде


class UserResponse(BaseModel):
    """Схема ответа с данными пользователя"""
    id: int
    email: EmailStr
    role: UserRole = UserRole.USER
    is_active: bool
    created_at: Optional[datetime]  # Дата регистрации
    last_active_at: Optional[datetime]  # Последняя активность


class UserLogin(BaseModel):
    """Схема входа пользователя в систему"""
    email: EmailStr
    password: str  # Пароль в открытом виде
