import pytest
import httpx

from resty.enums import Method
from resty.types import Request, Response
from resty.clients.httpx import RESTClient
from resty.middlewares import BaseRequestMiddleware, BaseResponseMiddleware
from resty.exceptions import ConnectError

from tests.clients.conftest import HTTPXAsyncClientMock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "base",
    [
        BaseRequestMiddleware,
        BaseResponseMiddleware,
    ],
)
async def test_middlewares_calling(
    base,
):
    class Mid(base):

        def __init__(self):
            self.called = False

        async def __call__(self, request: Request, **kwargs):
            self.called = True

    mid = Mid()

    client = RESTClient(HTTPXAsyncClientMock(httpx.Response(status_code=200)))
    client.middlewares.add_middleware(mid)

    await client.request(
        Request(
            url="test",
            method=Method.GET,
        )
    )

    assert mid.called


@pytest.mark.asyncio
async def test_request():
    client = RESTClient(
        HTTPXAsyncClientMock(httpx.Response(status_code=123)), check_status=False
    )
    print(client.middlewares.middlewares)

    response = await client.request(Request(url="test", method=Method.GET))

    assert isinstance(response, Response)
    assert response.status == 123


@pytest.mark.asyncio
async def test_connection_error():
    client = RESTClient(
        HTTPXAsyncClientMock(
            httpx.Response(status_code=123), error=httpx.ConnectError("test")
        ),
        check_status=False,
    )

    with pytest.raises(ConnectError):
        await client.request(Request(url="test", method=Method.GET))
