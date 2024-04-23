from typing import Iterable

from resty.types import (
    BaseMiddlewareManager,
    BaseMiddleware,
    BaseRequestMiddleware,
    BaseResponseMiddleware,
)

from resty.types import Request, Response


class MiddlewareManager(BaseMiddlewareManager):
    def __init__(self, middlewares: Iterable[BaseMiddleware] = None):
        if not middlewares:
            middlewares = []
        for middleware in middlewares:
            self.add_middleware(middleware=middleware)

        self._middlewares = []

    async def call_request_middlewares(self, request: Request, **context):
        for middleware in self._middlewares:
            if isinstance(middleware, BaseRequestMiddleware):
                await middleware.handle_request(request=request, **context)

    async def call_response_middlewares(self, response: Response, **context):
        for middleware in self._middlewares:
            if isinstance(middleware, BaseResponseMiddleware):
                await middleware.handle_response(response=response, **context)

    def add_middleware(self, middleware: BaseMiddleware):
        if not isinstance(middleware, BaseMiddleware):
            raise TypeError("middleware is not of type BaseMiddleware")
        self._middlewares.append(middleware)
