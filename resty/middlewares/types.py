from abc import ABC, abstractmethod
from typing import Iterable
from contextlib import contextmanager


class BaseMiddleware(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs): ...


class BaseRequestMiddleware(BaseMiddleware, ABC):
    @abstractmethod
    def __call__(self, request, **kwargs): ...


class BaseResponseMiddleware(BaseMiddleware, ABC):
    @abstractmethod
    def __call__(self, response, **kwargs): ...


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
    async def __call__(self, *args, base: type[BaseMiddleware] = BaseMiddleware, **kwargs): ...
