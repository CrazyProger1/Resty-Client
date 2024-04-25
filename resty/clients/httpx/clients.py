import json

import httpx

from resty.clients.types import (
    BaseRESTClient,
    Request,
    Response,
)
from resty.middlewares import (
    MiddlewareManager,
    BaseRequestMiddleware,
    BaseResponseMiddleware,
    StatusCheckingMiddleware,
)
from resty.exceptions import ConnectError


class RESTClient(BaseRESTClient):
    middlewares = MiddlewareManager()

    def __init__(self, httpx_client: httpx.AsyncClient = None, check_status: bool = True):
        self._xclient = httpx_client or httpx.AsyncClient()

        if check_status:
            self.middlewares.add_middleware(StatusCheckingMiddleware())

    async def _make_xrequest(self, request: Request) -> httpx.Response:
        try:
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
        except httpx.ConnectError:
            raise ConnectError(url=request.url)

    @staticmethod
    def _extract_json_data(xresponse: httpx.Response) -> dict | list:
        try:
            data = xresponse.json()
        except json.decoder.JSONDecodeError:
            data = {}

        return data

    async def _parse_xresponse(self, request: Request, xresponse: httpx.Response) -> Response:
        return Response(
            request=request,
            status=xresponse.status_code,
            json=self._extract_json_data(xresponse=xresponse),
            content=xresponse.content,
            text=xresponse.text,
            middleware_options=request.middleware_options
        )

    async def _make_request(self, request: Request) -> Response:
        xresponse = await self._make_xrequest(request=request)
        response = await self._parse_xresponse(request=request, xresponse=xresponse)
        return response

    async def _call_middlewares(self, reqresp: Request | Response):
        await self.middlewares(
            reqresp,
            base=BaseRequestMiddleware if isinstance(reqresp, Request) else BaseResponseMiddleware,
            **reqresp.middleware_options
        )

    async def request(self, request: Request) -> Response:
        await self._call_middlewares(reqresp=request)

        response = await self._make_request(request)

        await self._call_middlewares(reqresp=response)

        return response
