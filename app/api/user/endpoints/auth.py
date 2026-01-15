from fastapi import APIRouter, status, Depends, Request, BackgroundTasks

from app.dependencies import get_auth_service, get_session_service
from app.core.exceptions import BadRequestException, UnauthorizedException
from app.services.session import SessionService
from app.schemas.user import UserLogin
from app.schemas.token import RefreshTokenRequest, UserTokens
from app.services.auth import AuthService


router = APIRouter(tags=['User | Auth'])



@router.post('/register', response_model=UserTokens, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserLogin,
    request: Request,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(get_auth_service),
    session_service: SessionService = Depends(get_session_service),
) -> UserTokens:
    """Регистрация нового пользователя"""
    try:
        user = await auth_service.register(user_data)
    except ValueError as e:
        raise BadRequestException(str(e))

    tokens = await auth_service.create_tokens(user)

    # Сохранение информации о сессии
    background_tasks.add_task(
        session_service.create_login_session,
        user_id=user.id,
        refresh_token=tokens.refresh_token,
        ip_address=request.client.host,
        user_agent=request.headers.get('user-agent')
    )
    return tokens


@router.post('/login', response_model=UserTokens)
async def login(
    user_data: UserLogin,
    request: Request,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(get_auth_service),
    session_service: SessionService = Depends(get_session_service),
) -> UserTokens:
    """Вход в систему"""
    user = await auth_service.login(user_data)
    if not user:
        raise UnauthorizedException('Неверный email или пароль')

    tokens = await auth_service.create_tokens(user)

    # Сохранение информации о сессии
    background_tasks.add_task(
        session_service.create_login_session,
        user_id=user.id,
        refresh_token=tokens.refresh_token,
        ip_address=request.client.host,
        user_agent=request.headers.get('user-agent')
    )
    return tokens


@router.post('/refresh', response_model=UserTokens)
async def refresh_tokens(
    refresh_data: RefreshTokenRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(get_auth_service),
    session_service: SessionService = Depends(get_session_service),
) -> UserTokens:
    """Обновление токенов"""
    tokens = await auth_service.refresh_tokens(refresh_data.token)
    if not tokens:
        raise UnauthorizedException('Недействительный refresh токен')

    # Сохранение информации о сессии
    background_tasks.add_task(
        session_service.update_login_session,
        refresh_token=tokens.refresh_token,
        ip_address=request.client.host,
    )
    return tokens


@router.post('/logout')
async def logout(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Выход из системы"""
    success = await auth_service.logout(refresh_data.token)
    return {'message': 'Успешный выход из системы' if success else 'Неудачный выход из системы'}


@router.post('/logout-all')
async def logout_all(
    user_id: int,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Выход из всех устройств"""
    await auth_service.logout_all(user_id)
    return {'message': 'Успешный выход из всех устройств'}
