import json.decoder
from typing import Container

import httpx

from resty.constants import DEFAULT_CODES, STATUS_ERRORS
from resty.types import (
    BaseRESTClient,
    Request,
    Response,
    BaseMiddleware,
    BaseMiddlewareManager,
)
from resty.exceptions import HTTPError
from resty.middlewares import MiddlewareManager


class RESTClient(BaseRESTClient):

    def __init__(
            self,
            xclient: httpx.AsyncClient = None,
            middleware_manager: BaseMiddlewareManager = None,
    ):

        self._xclient = xclient or httpx.AsyncClient()
        self._middleware_manager = middleware_manager or MiddlewareManager()

    @staticmethod
    def _parse_xresponse(xresponse: httpx.Response) -> dict | list | None:
        try:
            data = xresponse.json()
        except json.decoder.JSONDecodeError:
            data = {}

        return data

    @staticmethod
    def _check_status(
            status: int,
            expected_status: int | Container[int],
            request: Request,
            url: str,
            data: dict = None,
    ):
        if status != expected_status:
            if isinstance(expected_status, Container) and status in expected_status:
                pass
            else:
                exc: type[HTTPError] = STATUS_ERRORS.get(status, HTTPError)
                raise exc(request=request, status=status, url=url, data=data)

    async def _make_xrequest(self, request: Request):
        return await self._xclient.request(
            method=request.method.value,
            url=request.url,
            headers=request.headers,
            json=request.json,
            data=request.data,
            params=request.params,
            cookies=request.cookies,
            follow_redirects=request.redirects,
            timeout=request.timeout,
        )

    def add_middleware(self, middleware: BaseMiddleware):
        self._middleware_manager.add_middleware(middleware=middleware)

    async def request(self, request: Request, **context) -> Response:
        if not isinstance(request, Request):
            raise TypeError("request is not of type Request")

        expected_status: int = context.pop(
            "expected_status", DEFAULT_CODES.get(request.method)
        )
        check_status: bool = context.pop("check_status", True)

        if not isinstance(expected_status, (int, Container)):
            raise TypeError("expected status should be type of int or Container[int]")

        await self._middleware_manager.call_request_middlewares(
            request=request, **context
        )

        xresponse = await self._make_xrequest(request=request)

        data = self._parse_xresponse(xresponse=xresponse)

        status = xresponse.status_code

        if check_status:
            self._check_status(
                status=status,
                expected_status=expected_status,
                request=request,
                url=str(xresponse.url),
                data=data,
            )
        response = Response(
            request=request,
            status=status,
            data=data,
        )

        await self._middleware_manager.call_response_middlewares(
            response=response, **context
        )

        return response
