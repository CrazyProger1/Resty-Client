import json.decoder
from typing import Container

import httpx

from resty.constants import (
    DEFAULT_CODES,
    STATUS_ERRORS
)
from resty.types import (
    BaseRESTClient,
    Request,
    Response,
    BaseMiddleware,
    BaseMiddlewareManager
)
from resty.exceptions import (
    HTTPError,
    ParsingError
)
from resty.middlewares import MiddlewareManager


class RESTClient(BaseRESTClient):

    def __init__(self, xclient: httpx.AsyncClient, middleware_manager: BaseMiddlewareManager = None):
        self._xclient = xclient
        self._middleware_manager = middleware_manager or MiddlewareManager()

    @staticmethod
    def _parse_xresponse(xresponse: httpx.Response) -> dict | list | None:
        try:
            data = xresponse.json()
        except json.decoder.JSONDecodeError:
            data = None

            if xresponse.status_code != 204:
                raise ParsingError()
        return data

    @staticmethod
    def _check_status(status: int, expected_status: int | Container[int], request: Request):
        if status != expected_status:
            if isinstance(expected_status, Container) and status in expected_status:
                pass
            else:
                exc: type[HTTPError] = STATUS_ERRORS.get(status, HTTPError)
                raise exc(
                    request=request,
                    status=status
                )

    def add_middleware(self, middleware: BaseMiddleware):
        self._middleware_manager.add_middleware(middleware=middleware)

    async def request(self, request: Request, **kwargs) -> Response:
        if not isinstance(request, Request):
            raise TypeError('request is not of type Request')

        expected_status: int = kwargs.pop('expected_status', DEFAULT_CODES.get(request.method))

        if not isinstance(expected_status, (int, Container[int])):
            raise TypeError('expected status should be type of int or Container[int]')

        await self._middleware_manager.call_pre_middlewares(request=request, **kwargs)

        xresponse = await self._xclient.request(
            method=request.method.value,
            url=request.url,
            headers=request.headers,
            data=request.data,
            params=request.params,
            cookies=request.cookies,
            follow_redirects=request.redirects,
            timeout=request.timeout
        )

        status = xresponse.status_code
        self._check_status(
            status=status,
            expected_status=expected_status,
            request=request
        )

        response = Response(
            request=request,
            status=status,
            data=self._parse_xresponse(
                xresponse=xresponse
            )
        )
        await self._middleware_manager.call_post_middlewares(response=response, **kwargs)

        return response
