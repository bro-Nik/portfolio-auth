from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
    password_hash: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
