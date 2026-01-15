from typing import Any, Callable, TypeVar, cast
import functools
from fastapi import HTTPException, status
from pydantic import ValidationError



F = TypeVar('F', bound=Callable[..., Any])


def service_exception_handler(default_message: str = 'Ошибка при выполнении операции'):
    """Фабрика декораторов для обработки исключений сервисов"""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except PermissionDeniedError as e:
                raise ForbiddenException(str(e))
            except NotFoundError as e:
                raise NotFoundException(str(e))
            except ConflictError as e:
                raise ConflictException(str(e))
            except ValidationError as e:
                # Все ошибки в виде строки
                error_messages = [err['msg'] for err in e.errors()]
                raise ValidationException(str(error_messages))
            except Exception as e:
                raise BadRequestException(f'{default_message}: {str(e)}')
        return cast(F, wrapper)
    return decorator


class BadRequestException(HTTPException):
    """400 - Неверный запрос"""
    def __init__(self, detail: str = 'Неверный запрос'):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class UnauthorizedException(HTTPException):
    """401 - Не авторизован"""
    def __init__(self, detail: str = 'Необходима авторизация'):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'}
        )


class ForbiddenException(HTTPException):
    """403 - Нет разрешения"""
    def __init__(self, detail: str = 'Недостаточно прав'):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class NotFoundException(HTTPException):
    """404 - Не найдено"""
    def __init__(self, detail: str = 'Ресурс не найден'):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ConflictException(HTTPException):
    """409 - Коннфликт"""
    def __init__(self, detail: str = 'Конфликт данных'):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class ValidationException(HTTPException):
    """422 - Ошибка валидации"""
    def __init__(self, detail: str = 'Ошибка валидации'):
        super().__init__(
            status_code=422,
            detail=detail
        )


class BusinessException(Exception):
    """Базовое бизнес-исключение"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class PermissionDeniedError(BusinessException):
    """Недостаточно прав"""
    def __init__(self, message: str = "Недостаточно прав"):
        super().__init__(message)


class NotFoundError(BusinessException):
    """Ресурс не найден"""
    def __init__(self, message: str):
        super().__init__(message)


class ConflictError(BusinessException):
    """Конфликт (уже существует)"""
    def __init__(self, message: str):
        super().__init__(message)


class BusinessValidationError(BusinessException):
    """Ошибка валидации"""
    def __init__(self, message: str):
        super().__init__(message)
