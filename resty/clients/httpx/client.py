import json.decoder

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
    BasePreRequestMiddleware,
    BasePostRequestMiddleware
)
from resty.exceptions import HTTPError


class RESTClient(BaseRESTClient):

    def __init__(self, xclient: httpx.AsyncClient):
        self._xclient = xclient
        self._middlewares = []

    async def _call_pre_middlewares(self, request: Request, **kwargs):
        for middleware in self._middlewares:
            if isinstance(middleware, BasePreRequestMiddleware):
                await middleware.handle_request(request=request, **kwargs)

    async def _call_post_middlewares(self, response: Response, **kwargs):
        for middleware in self._middlewares:
            if isinstance(middleware, BasePostRequestMiddleware):
                await middleware.handle_response(response=response, **kwargs)

    def add_middleware(self, middleware: BaseMiddleware):
        if not isinstance(middleware, BaseMiddleware):
            raise TypeError('middleware is not of type BaseMiddleware')
        self._middlewares.append(middleware)

    async def request(self, request: Request, **kwargs) -> Response:
        if not isinstance(request, Request):
            raise TypeError('request is not of type Request')

        expected_status: int = kwargs.pop('expected_status', DEFAULT_CODES.get(request.method))
        await self._call_pre_middlewares(request=request, **kwargs)

        xresponse = await self._xclient.request(
            method=request.method.value,
            url=request.url,
            headers=request.headers,
            data=request.data,
            params=request.params
        )

        status = xresponse.status_code

        if status != expected_status:
            exc: type[HTTPError] = STATUS_ERRORS.get(status, HTTPError)
            raise exc(
                request=request,
                status=status
            )

        try:
            data = xresponse.json()
        except json.decoder.JSONDecodeError:
            data = None

            if status != 204:
                raise

        response = Response(
            request=request,
            status=status,
            data=data
        )
        await self._call_post_middlewares(response=response, **kwargs)
        return response
