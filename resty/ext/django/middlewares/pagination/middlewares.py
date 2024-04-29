from abc import ABC, abstractmethod
from typing import Container

from resty.enums import Endpoint
from resty.types import Request, Response
from resty.middlewares import BaseRequestMiddleware, BaseResponseMiddleware

from .constants import DEFAULT_LIMIT


class PaginationMiddleware(BaseRequestMiddleware, BaseResponseMiddleware, ABC):
    def __init__(self, endpoints: Container[Endpoint] = None):
        self._endpoints = endpoints or {
            Endpoint.READ,
        }

    @abstractmethod
    async def paginate(self, request: Request, **kwargs):  # pragma: nocover
        ...

    async def unpaginate(self, response: Response, **kwargs):
        response.json = response.json.get("results", response.json)

    async def _handle_request(self, request: Request, **kwargs):
        if request.endpoint in self._endpoints:
            await self.paginate(request=request, **kwargs)

    async def _handle_response(self, response: Response, **kwargs):
        if response.request.endpoint in self._endpoints:
            await self.unpaginate(response=response, **kwargs)

    async def __call__(self, reqresp: Request | Response, **kwargs):
        if isinstance(reqresp, Request):
            return await self._handle_request(request=reqresp, **kwargs)
        return await self._handle_response(response=reqresp, **kwargs)


class LimitOffsetPaginationMiddleware(PaginationMiddleware):
    def __init__(self, limit: int = DEFAULT_LIMIT, **kwargs):
        self._limit = limit
        super().__init__(**kwargs)

    async def paginate(self, request: Request, **kwargs):
        request.params.update(
            {
                "limit": kwargs.pop("limit", self._limit),
                "offset": kwargs.pop("offset", 0),
            }
        )


class PagePaginationMiddleware(PaginationMiddleware):
    async def paginate(self, request: Request, **kwargs):
        request.params.update(
            {
                "page": kwargs.pop("page", 1),
            }
        )
