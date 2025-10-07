# import time
from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies import get_auth_service
from app.models.user import UserLogin
from app.models.token import Token
from app.services.auth import AuthService


router = APIRouter()


@router.post('/register', response_model=Token)
async def register(user_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    """Регистрация нового пользователя"""
    # try:
    user = await auth_service.register_user(user_data)
    return await auth_service.create_tokens(user)
    # except ValueError as e:
    #     raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


