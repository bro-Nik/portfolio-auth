from typing import Callable, Any
from functools import wraps

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import SecurityService
from app.services.auth import AuthService
from app.schemas import UserRole


security = HTTPBearer()

from app.dependencies import get_db
from app.services.auth import AuthService


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Зависимость для получения сервиса аутентификации"""
    return AuthService(db)


def require_role(required_role: UserRole):
    """Декоратор для проверки роли пользователя"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(
            *args,
            user_role: UserRole = Depends(get_current_user_role),
            **kwargs
        ) -> Any:
            if required_role.priority > user_role.priority:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f'Недостаточно прав доступа. Требуется роль: {required_role.value}'
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Получить payload из токена"""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не авторизован'
        )

    token = credentials.credentials
    payload = SecurityService.verify_token(token)

    if payload is None or payload.get('type') != 'access':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверные учетные данные для аутентификации',
        )

    return payload


def get_current_user_role(
    payload: dict = Depends(get_current_user_payload)
) -> UserRole:
    """Получить роль пользователя"""
    role = payload.get('role', 'user')
    try:
        return UserRole(role)
    except ValueError:
        return UserRole.USER
