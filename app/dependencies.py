from typing import List
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import SecurityService
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.db.connection import db
from app.repositories.token import TokenRepository
from app.services.auth import AuthService
from app.services.admin import AdminService
from app.models.user import UserRole, User


security = HTTPBearer()


def get_user_repository() -> UserRepository:
    """Зависимость для получения репозитория пользователей"""
    return UserRepository(db.pool)


def get_auth_service() -> AuthService:
    """Зависимость для получения сервиса аутентификации"""
    user_repo = UserRepository(db.pool)
    token_repo = TokenRepository(db.pool)
    return AuthService(user_repo, token_repo)


def get_admin_service() -> AdminService:
    """Зависимость для получения сервиса администратора"""
    user_repo = UserRepository(db.pool)
    token_repo = TokenRepository(db.pool)
    return AdminService(user_repo, token_repo)


def require_role(required_role: UserRole):
    """Декоратор для проверки роли пользователя"""
    def role_checker(
        user_roles: List[UserRole] = Depends(get_current_user_roles)
    ):
        if required_role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {required_role.value}"
            )
        return user_roles
    return role_checker


def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Получить payload из токена"""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован"
        )

    token = credentials.credentials
    payload = SecurityService.verify_token(token)

    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return payload


def get_current_user_roles(
    payload: dict = Depends(get_current_user_payload)
) -> List[UserRole]:
    """Получить роли пользователя"""
    roles = payload.get("roles", [])
    try:
        return [UserRole(role) for role in roles]
    except ValueError:
        return [UserRole.USER]


async def get_current_user(
    payload: dict = Depends(get_current_user_payload)
) -> dict:
    """Зависимость для получения текущего пользователя"""
    user_id = int(payload["sub"])
    user_repo = UserRepository(db.pool)
    user_service = UserService(user_repo)

    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
