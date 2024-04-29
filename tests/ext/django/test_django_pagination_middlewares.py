import pytest

from resty.enums import Method, Endpoint
from resty.types import Request, Response
from resty.ext.django.middlewares.pagination import (
    LimitOffsetPaginationMiddleware,
    PagePaginationMiddleware,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "req, kwargs, expected",
    [
        (
            Request(
                url="https://example.com/", method=Method.GET, endpoint=Endpoint.READ
            ),
            {"limit": 100, "offset": 10},
            {"limit": 100, "offset": 10},
        )
    ],
)
async def test_limit_offset_pagination(req, kwargs, expected):
    middleware = LimitOffsetPaginationMiddleware()

    await middleware(reqresp=req, **kwargs)

    assert req.params == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "req, kwargs, expected",
    [
        (
            Request(
                url="https://example.com/", method=Method.GET, endpoint=Endpoint.READ
            ),
            {"page": 100},
            {"page": 100},
        )
    ],
)
async def test_page_pagination(req, kwargs, expected):
    middleware = PagePaginationMiddleware()

    await middleware(reqresp=req, **kwargs)

    assert req.params == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "middleware, resp, expected",
    [
        (
            LimitOffsetPaginationMiddleware(),
            Response(
                request=Request(
                    url="https://example.com/",
                    method=Method.GET,
                    endpoint=Endpoint.READ,
                ),
                status=200,
                json={
                    "results": [
                        {"id": 1, "username": "josh"},
                    ]
                },
            ),
            [
                {"id": 1, "username": "josh"},
            ],
        ),
        (
            PagePaginationMiddleware(),
            Response(
                request=Request(
                    url="https://example.com/",
                    method=Method.GET,
                    endpoint=Endpoint.READ,
                ),
                status=200,
                json={
                    "results": [
                        {"id": 1, "username": "josh"},
                    ]
                },
            ),
            [
                {"id": 1, "username": "josh"},
            ],
        ),
    ],
)
async def test_unpaginate(middleware, resp, expected):
    await middleware(reqresp=resp)
    assert resp.json == expected
