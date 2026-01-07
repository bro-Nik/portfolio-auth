from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies import get_auth_service
from app.schemas.user import UserLogin
from app.schemas.token import RefreshTokenRequest, UserTokens
from app.services.auth import AuthService


router = APIRouter()


@router.post('/register', response_model=UserTokens, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserTokens:
    """Регистрация нового пользователя"""
    try:
        user = await auth_service.register(user_data)
        tokens = await auth_service.create_tokens(user)
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post('/login', response_model=UserTokens)
async def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserTokens:
    """Вход в систему"""
    user = await auth_service.login(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный email или пароль',
        )

    tokens = await auth_service.create_tokens(user)
    return tokens


@router.post('/refresh', response_model=UserTokens)
async def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> UserTokens:
    """Обновление токенов"""
    tokens = await auth_service.refresh_tokens(request.token)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Недействительный refresh токен',
        )

    return tokens


@router.post('/logout')
async def logout(
    refresh_token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Выход из системы"""
    await auth_service.logout(refresh_token)
    return {'message': 'Успешный выход из системы'}


@router.post('/logout-all')
async def logout_all(
    user_id: int,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Выход из всех устройств"""
    await auth_service.logout_all(user_id)
    return {'message': 'Успешный выход из всех устройств'}
