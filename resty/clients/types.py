from abc import ABC, abstractmethod

from resty.middlewares import BaseMiddlewareManager
from resty.types import Request, Response


class BaseRESTClient(ABC):
    middlewares: BaseMiddlewareManager

    @abstractmethod
    async def request(self, request: Request) -> Response: ...
