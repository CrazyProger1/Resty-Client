from resty.enums import Method
from resty.types import BaseRESTClient, Request, Response, BaseMiddleware


class MockRESTClient(BaseRESTClient):
    def __init__(self, status: int, data, method: Method, expected_url: str, expected_json=None):
        self.data = data
        self.status = status
        self.method = method
        self.expected_url = expected_url
        self.expected_json = expected_json

    def add_middleware(self, middleware: BaseMiddleware): ...

    async def request(self, request: Request, **context) -> Response:
        assert request.method == self.method
        assert request.url == self.expected_url
        if self.expected_json is not None:
            assert request.json == self.expected_json

        return Response(request=request, status=self.status, data=self.data)
