import time
from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies import get_auth_service, get_admin_service, require_role
from app.models.user import UserRole
from app.services.admin import AdminService


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
async def get_users(
    admin_service: AdminService = Depends(get_admin_service),
    _ = Depends(require_role(UserRole.ADMIN))
):
    time.sleep(1)  # ToDo
    users = await admin_service.get_users()
    return users
