from typing import Annotated

from app.core.responses import COMMON_RESPONSES, WRITE_RESPONSES
from fastapi import APIRouter, Depends, Path, Query, status

from app.core.exceptions import service_exception_handler
from app.dependencies import get_auth_service, get_user_service
from app.schemas import UserResponse, UserRole
from app.schemas.user import UserCreateRequest, UserLogoutAllRequest, UserUpdateRequest
from app.services.auth import AuthService
from app.services.user import UserService


router = APIRouter( prefix='/users', tags=['Admin | Users'], responses=COMMON_RESPONSES)


@router.get('/')
@service_exception_handler('Ошибка при получении пользователей')
async def get_users(
    service: Annotated[UserService, Depends(get_user_service)],
    skip: Annotated[int, Query(ge=0, description='Количество записей для пропуска')] = 0,
    limit: Annotated[int, Query(ge=1, le=1000, description='Лимит записей')] = 100,
    search: Annotated[str | None, Query(description='Поиск по email')] = None,
    role: Annotated[UserRole | None, Query(description='Фильтр по роли')] = None,
) -> list[UserResponse]:
    """Получить список пользователей с пагинацией и фильтрацией."""
    return await service.get_users_with_details(skip, limit, search, role)


@router.get('/{user_id}')
@service_exception_handler('Ошибка при получении пользователя')
async def get_user(
    user_id: Annotated[int, Path(..., description='ID пользователя')],
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    """Получить пользователя по ID."""
    return await service.get_user_with_details(user_id)


@router.post('/', status_code=status.HTTP_201_CREATED, responses=WRITE_RESPONSES)
@service_exception_handler('Ошибка при создании пользователя')
async def create_user(
    user_data: UserCreateRequest,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    """Создать нового пользователя."""
    user = await service.create_user(user_data)
    return await service.get_user_with_details(user.id)


@router.put('/{user_id}', responses=WRITE_RESPONSES)
@service_exception_handler('Ошибка при изменении пользователя')
async def update_user(
    user_id: Annotated[int, Path(..., description='ID пользователя')],
    user_data: UserUpdateRequest,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    """Обновить пользователя."""
    user = await service.update_user(user_id, user_data)
    return await service.get_user_with_details(user.id)


@router.delete('/{user_id}', status_code=204, responses=WRITE_RESPONSES)
@service_exception_handler('Ошибка при удалении пользователя')
async def delete_user(
    user_id: Annotated[int, Path(..., description='ID пользователя')],
    service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    """Удалить пользователя."""
    await service.delete_user(user_id)


@router.post('/logout-all')
@service_exception_handler('Ошибка при выходе из всех устройств')
async def logout_all(
    data: UserLogoutAllRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:
    """Выход из всех устройств."""
    await auth_service.logout_all(data.user_id)
    return {'message': 'Успешный выход из всех устройств'}
