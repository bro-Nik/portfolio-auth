from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Схема для ошибок."""

    message: str = Field(..., description='Описание ошибки')
