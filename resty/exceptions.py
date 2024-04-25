from resty.types import Response


class RestyError(Exception):
    pass


class URLFormattingError(RestyError):
    pass


class HTTPError(RestyError):
    def __init__(self, response: Response):
        self.response = response
        super().__init__(f"{response.request.method.value}: {response.request.url} -> {response.status}")


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
