from resty.types import Request


class HTTPError(Exception):
    def __init__(self, request: Request, status: int, url: str, data: dict):
        self.request = request
        self.status = status
        self.url = url
        self.data = data
        super().__init__(f"{request.method.value}: {url} -> {status}")


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
