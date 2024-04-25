from resty.enums import Method
from resty.types import BaseRESTClient, Request, Response, BaseMiddleware


class MockRESTClient(BaseRESTClient):
    def __init__(
            self,
            status: int = None,
            data=None,
            **expected
    ):
        self.return_data = data
        self.return_status = status
        self.expected = expected

    def add_middleware(self, middleware: BaseMiddleware): ...

    async def request(self, request: Request, **context) -> Response:
        for attrname, expected_value in self.expected.items():
            assert getattr(request, attrname.removeprefix('expected_')) == expected_value

        return Response(
            request=request, status=self.return_status, data=self.return_data
        )
