from resty.types import Response


class RestyError(Exception):
    pass


class NetworkError(RestyError):
    pass


class URLBuildingError(RestyError):
    pass


class ConnectError(NetworkError, ConnectionError):
    def __init__(self, url: str):
        self.url = url  # pragma: no cover
        super().__init__(
            f"Failed to establish a connection to the server {url}"
        )  # pragma: no cover


class HTTPError(NetworkError):
    def __init__(self, response: Response):
        self.response = response  # pragma: no cover
        super().__init__(  # pragma: no cover
            f"{response.request.method.value}: {response.request.url} -> {response.status}"
        )


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
