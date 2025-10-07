from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import jwt
from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityService:
    """Сервис для работы с безопасностью"""

    @staticmethod
    def access_token_expires() -> datetime:
        return datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    @staticmethod
    def refresh_token_expires() -> datetime:
        return datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    @staticmethod
    def create_access_token(user_id: int) -> str:
        token_payload: Dict[str, Any] = {
            "sub": str(user_id),
            "type": "access",
            "exp": SecurityService.access_token_expires()
        }

        access_token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return access_token

    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        token_payload: Dict[str, Any] = {
            "sub": str(user_id),
            "type": "refresh", 
            "exp": SecurityService.refresh_token_expires()
        }

        refresh_token = jwt.encode(token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return refresh_token

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.JWTError:
            return None
