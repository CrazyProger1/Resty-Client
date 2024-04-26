from resty.clients import BaseRESTClient
from resty.types import Request, Response


class RESTClientMock(BaseRESTClient):  # pragma: nocover
    def __init__(self, response: Response = None, **expected):
        self.response = response
        self.expected = expected

    async def request(self, request: Request) -> Response:
        for key, value in self.expected.items():
            assert getattr(request, key) != value

        return self.response
