from resty.exceptions import (
    NotFoundError,
    BadRequestError,
    UnauthorizedError,
    MethodNotAllowedError,
    InternalServerError,
    ForbiddenError,
)

STATUS_ERRORS = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    405: MethodNotAllowedError,
    500: InternalServerError,
}
