from fastapi import APIRouter, HTTPException, status, Depends
import time

from app.dependencies import get_auth_service, get_current_user
from app.models.user import UserLogin
from app.models.token import RefreshTokenRequest, Token
from app.services.auth import AuthService


router = APIRouter()


@router.post('/register', response_model=Token)
async def register(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    """Регистрация нового пользователя"""
    try:
        user = await auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    tokens = await auth_service.create_tokens(user)
    return tokens


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    """Вход в систему"""
    time.sleep(2)  # ToDo защита от подбора

    user = await auth_service.login_user(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    tokens = await auth_service.create_tokens(user)
    return tokens


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    """Обновление токенов"""
    tokens = await auth_service.refresh_tokens(request.token)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    return tokens


# @router.get("/me")
# async def get_current_user_info(current_user: dict = Depends(get_current_user)):
#     time.sleep(1)  # ToDo
#     return current_user


# @router.post("/logout")
# async def logout(refresh_token: str, auth_service: AuthService = Depends(get_auth_service)):
#     """Выход из системы"""
#     auth_service.logout(refresh_token)
#     return {"message": "Successfully logged out"}
#
#
# @router.post("/logout-all")
# async def logout_all(user_id: int, auth_service: AuthService = Depends(get_auth_service)):
#     """Выход из всех устройств"""
#     auth_service.logout_all(user_id)
#     return {"message": "Successfully logged out from all devices"}
