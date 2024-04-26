from typing import Iterable
from contextlib import contextmanager
from abc import ABC, abstractmethod

from resty.types import Request, Response


class BaseMiddleware(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs): ...


class BaseRequestMiddleware(BaseMiddleware, ABC):
    @abstractmethod
    def __call__(self, request: Request, **kwargs): ...


class BaseResponseMiddleware(BaseMiddleware, ABC):
    @abstractmethod
    def __call__(self, response: Response, **kwargs): ...


class BaseMiddlewareManager(ABC):
    @property
    @abstractmethod
    def middlewares(self) -> Iterable[BaseMiddleware]: ...

    @abstractmethod
    def add_middleware(self, middleware: BaseMiddleware): ...

    @abstractmethod
    def add_middlewares(self, *middlewares: BaseMiddleware): ...

    @abstractmethod
    def remove_middleware(self, middleware: BaseMiddleware): ...

    @abstractmethod
    def remove_middlewares(self, *middlewares: BaseMiddleware): ...

    @contextmanager
    @abstractmethod
    def middleware(self, *middlewares: BaseMiddleware): ...

    @abstractmethod
    async def __call__(
        self, *args, base: type[BaseMiddleware] = BaseMiddleware, **kwargs
    ): ...
