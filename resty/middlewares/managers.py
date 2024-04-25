from contextlib import contextmanager
from typing import Iterable

from resty.middlewares.types import BaseMiddlewareManager, BaseMiddleware


class MiddlewareManager(BaseMiddlewareManager):

    def __init__(self, middlewares: Iterable = None):
        self._middlewares = []

        self.add_middlewares(*middlewares or ())

    @property
    def middlewares(self) -> Iterable[BaseMiddleware]:
        return tuple(self._middlewares)

    def add_middleware(self, middleware: BaseMiddleware):
        if not isinstance(middleware, BaseMiddleware):
            raise TypeError('Middleware must inherit the base type BaseMiddleware')

        if middleware not in self._middlewares:
            self._middlewares.append(middleware)

    def add_middlewares(self, *middlewares: BaseMiddleware):
        for middleware in middlewares:
            self.add_middleware(middleware)

    def remove_middleware(self, middleware: BaseMiddleware):
        if middleware in self._middlewares:
            self._middlewares.remove(middleware)

    def remove_middlewares(self, *middlewares: BaseMiddleware):
        for middleware in middlewares:
            self.remove_middleware(middleware)

    @contextmanager
    def middleware(self, *middlewares: BaseMiddleware):
        self.add_middlewares(*middlewares)
        yield
        self.remove_middlewares(*middlewares)

    async def __call__(self, *args, base: type[BaseMiddleware] = BaseMiddleware, **kwargs):
        for middleware in self._middlewares:
            if isinstance(middleware, base):
                await middleware(*args, **kwargs)
