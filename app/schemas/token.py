from pydantic import BaseModel


class UserTokens(BaseModel):
    """Ответ с парой токенов (access + refresh)"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenCreate(BaseModel):
    """Схема для создания нового refresh токена"""
    user_id: int
    token: str
    expires_at: int


class RefreshTokenUpdate(BaseModel):
    """Схема для обновления существующего refresh токена"""
    new_token: str
    expires_at: int
    token_id: int


class RefreshTokenRequest(BaseModel):
    """Запрос на обновление access токена"""
    token: str
