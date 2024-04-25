from resty.types import Response


class RestyError(Exception):
    pass


class URLFormattingError(RestyError):
    pass


class ConnectError(RestyError):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f"Failed to establish a connection to the server {url}")


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
