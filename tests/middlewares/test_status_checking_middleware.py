import pytest

from resty.enums import Method
from resty.middlewares import StatusCheckingMiddleware
from resty.types import Response, Request


class CustomError(Exception):
    pass


class ErrorWithConstructor(Exception):
    def __init__(self):
        pass


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "expected_status, actual_status, error",
    [
        (200, 404, CustomError),
        ((200, 201), 401, CustomError),
        ((200, 204), 403, ErrorWithConstructor)
    ]
)
async def test_invalid_status_check(expected_status, actual_status, error):
    mid = StatusCheckingMiddleware(errors={actual_status: error})
    with pytest.raises(error):
        await mid(response=Response(
            request=Request(
                url="",
                method=Method.GET,
            ),
            status=actual_status,
            content=b"",
            text="",
            json={},
            middleware_options={}
        ),
            expected_status=expected_status
        )
