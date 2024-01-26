from typing import Iterable

from resty.types import (
    BaseMiddlewareManager,
    BaseMiddleware,
    BasePreRequestMiddleware,
    BasePostRequestMiddleware
)

from resty.types import (
    Request,
    Response
)


class MiddlewareManager(BaseMiddlewareManager):
    def __init__(self, default_middlewares: Iterable[BaseMiddleware] = None):
        if not default_middlewares:
            default_middlewares = []
        for middleware in default_middlewares:
            self.add_middleware(middleware=middleware)

        self._middlewares = []

    async def call_pre_middlewares(self, request: Request, **kwargs):
        for middleware in self._middlewares:
            if isinstance(middleware, BasePreRequestMiddleware):
                await middleware.handle_request(request=request, **kwargs)

    async def call_post_middlewares(self, response: Response, **kwargs):
        for middleware in self._middlewares:
            if isinstance(middleware, BasePostRequestMiddleware):
                await middleware.handle_response(response=response, **kwargs)

    def add_middleware(self, middleware: BaseMiddleware):
        if not isinstance(middleware, BaseMiddleware):
            raise TypeError('middleware is not of type BaseMiddleware')
        self._middlewares.append(middleware)
