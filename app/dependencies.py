# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# from app.core.security import SecurityService
from app.repositories.user import UserRepository
# from app.services.user_service import UserService
from app.db.connection import db
from app.repositories.token import TokenRepository
from app.services.auth import AuthService


# security = HTTPBearer()

# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
#     """Зависимость для получения текущего пользователя"""
#     token = credentials.credentials
#     payload = SecurityService.verify_token(token)
#
#     if not payload or payload.get("type") != "access":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     user_id = int(payload["user_id"])
#     user_repo = UserRepository(db.pool)
#     user_service = UserService(user_repo)
#
#     user = user_service.get_user_by_id(user_id)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found",
#         )
#
#     return user


def get_user_repository() -> UserRepository:
    """Зависимость для получения репозитория пользователей"""
    return UserRepository(db.pool)

def get_auth_service() -> AuthService:
    """Зависимость для получения сервиса аутентификации"""
    user_repo = UserRepository(db.pool)
    token_repo = TokenRepository(db.pool)
    return AuthService(user_repo, token_repo)
