from resty.enums import Method
from resty.exceptions import (
    NotFoundError,
    BadRequestError,
    UnauthorizedError,
    MethodNotAllowedError,
    InternalServerError,
    ForbiddenError,
)

DEFAULT_CODES = {
    Method.GET: 200,
    Method.POST: {201, 200},
    Method.PUT: 200,
    Method.PATCH: 200,
    Method.DELETE: {204, 200},
}

STATUS_ERRORS = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    405: MethodNotAllowedError,
    500: InternalServerError,
}
