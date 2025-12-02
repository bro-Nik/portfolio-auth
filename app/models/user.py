from typing import List
from enum import Enum
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'


class User(BaseModel):
    id: int
    email: EmailStr
    password_hash: str | None = None
    roles: List[UserRole] = [UserRole.USER]


class UserLogin(BaseModel):
    email: EmailStr
    password: str
