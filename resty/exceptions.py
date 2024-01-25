from resty.requests import Request


class HTTPError(Exception):
    def __init__(self, request: Request, status: int):
        self.request = request
        self.status = status
        super().__init__(f'{request.method.value}: {request.url} -> {status}')


class BadRequestError(HTTPError):
    pass


class UnauthorizedError(HTTPError):
    pass


class ForbiddenError(HTTPError):
    pass


class NotFoundError(HTTPError):
    pass


class MethodNotAllowedError(HTTPError):
    pass


class InternalServerError(HTTPError):
    pass
