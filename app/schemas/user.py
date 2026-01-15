from datetime import datetime, timezone
from typing import List, Optional
from enum import Enum
from app.schemas.session import LoginSessionResponse
from pydantic import BaseModel, EmailStr, ConfigDict, computed_field, validator
from app.core.config import settings


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
    password: str  # Пароль в открытом виде
    role: UserRole = UserRole.USER
    status: str


class UserUpdate(BaseModel):
    """Схема для обновления данных пользователя"""
    id: int
    email: EmailStr
    password: str  # Пароль в открытом виде


class UserCreateRequest(BaseModel):
    """Схема для входящих данных для создания нового пользователя"""
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER
    status: Optional[str] = 'active'

    @validator('email')
    def validate_email(cls, v):
        if not '@' in v:
            raise ValueError('Некорректный email')
        return v


class UserUpdateRequest(BaseModel):
    """Схема для входящих данных для изменения пользователя"""
    role: Optional[UserRole] = UserRole.USER
    status: Optional[str] = 'active'


class UserResponse(BaseModel):
    """Схема ответа с данными пользователя"""
    id: int
    email: EmailStr
    role: UserRole = UserRole.USER
    status: str
    created_at: Optional[datetime]  # Дата регистрации
    last_active_at: Optional[datetime]  # Последняя активность
    total_active_time: int  # Общее время на сайте в секундах
    login_sessions: Optional[List[LoginSessionResponse]] = None

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def online(self) -> bool:
        """На сайте ли сейчас пользователь"""
        if not self.last_active_at:
            return False

        time_diff = datetime.now(timezone.utc) - self.last_active_at
        return time_diff.total_seconds() < settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


class UserLogin(BaseModel):
    """Схема входа пользователя в систему"""
    email: EmailStr
    password: str  # Пароль в открытом виде


class UserLogoutAllRequest(BaseModel):
    user_id: int


class UserCreateInternal(BaseModel):
    email: EmailStr
    password_hash: str
    role: Optional[UserRole] = UserRole.USER
    status: Optional[str] = 'active'


class UserUpdateInternal(BaseModel):
    role: Optional[UserRole] = UserRole.USER
    status: Optional[str] = 'active'
