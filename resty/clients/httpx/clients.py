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


class RESTClient(BaseRESTClient):
    middlewares = MiddlewareManager()

    def __init__(self, httpx_client: httpx.AsyncClient = None, check_status: bool = True):
        self._xclient = httpx_client or httpx.AsyncClient()

        if check_status:
            self.middlewares.add_middleware(StatusCheckingMiddleware())

    async def _make_request(self, request: Request) -> Response:
        response = Response(
            data={},
            status=200,
            request=request,
            middleware_options=request.middleware_options,
        )
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
