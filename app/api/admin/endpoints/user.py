from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import require_role, get_user_service
from app.schemas import UserResponse, UserRole
from app.services.user import UserService


router = APIRouter(prefix="/users", tags=["users"])


@require_role(UserRole.ADMIN)
@router.get("/")
async def get_users(
    service: UserService = Depends(get_user_service)
) -> List[UserResponse]:
    """Список пользователей"""
    users = await service.get_users()
    return users
