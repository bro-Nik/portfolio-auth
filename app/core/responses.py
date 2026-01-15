from app.schemas.common import ErrorResponse


COMMON_RESPONSES = {
    400: {'model': ErrorResponse},
    401: {'model': ErrorResponse},
    403: {'model': ErrorResponse},
    404: {'model': ErrorResponse},
    422: {'model': ErrorResponse},
    500: {'model': ErrorResponse},
}

WRITE_RESPONSES = {
    409: {'model': ErrorResponse},
}
