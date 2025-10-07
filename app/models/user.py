from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
