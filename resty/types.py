from abc import ABC, abstractmethod
from typing import Iterable
from dataclasses import (
    dataclass,
    field
)

from pydantic import BaseModel

from resty.enums import (
    Endpoint,
    Field
)
from resty.enums import (
    Method
)


@dataclass
class Request:
    url: str
    method: Method
    data: dict = None
    timeout: int = None
    params: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    cookies: dict = field(default_factory=dict)
    redirects: bool = False


@dataclass
class Response:
    request: Request
    status: int
    data: dict = None


class BaseMiddleware(ABC):
    pass


class BasePreRequestMiddleware(BaseMiddleware):
    @abstractmethod
    async def handle_request(self, request: Request, **kwargs): ...


class BasePostRequestMiddleware(BaseMiddleware):
    @abstractmethod
    async def handle_response(self, response: Response, **kwargs): ...


class BaseMiddlewareManager(ABC):
    @abstractmethod
    async def call_pre_middlewares(self, request: Request, **kwargs): ...

    @abstractmethod
    async def call_post_middlewares(self, response: Response, **kwargs): ...

    @abstractmethod
    def add_middleware(self, middleware: BaseMiddleware): ...


class BaseRESTClient(ABC):
    @abstractmethod
    def add_middleware(self, middleware: BaseMiddleware): ...

    @abstractmethod
    async def request(self, request: Request, **kwargs) -> Response: ...


class BaseSerializer:
    schema: type[BaseModel]

    @classmethod
    @abstractmethod
    def serialize(cls, obj: BaseModel) -> dict: ...

    @classmethod
    @abstractmethod
    def deserialize(cls, data: dict) -> BaseModel: ...


class BaseManager:
    serializer: type[BaseSerializer]
    endpoints: dict[Endpoint, str]
    fields: dict[Field, str]

    @classmethod
    @abstractmethod
    async def create(cls, client: BaseRESTClient, obj: BaseModel, **kwargs) -> BaseModel: ...

    @classmethod
    @abstractmethod
    async def read(cls, client: BaseRESTClient, **kwargs) -> Iterable[BaseModel]: ...

    @classmethod
    @abstractmethod
    async def read_one(cls, client: BaseRESTClient, pk: any, **kwargs) -> BaseModel: ...

    @classmethod
    @abstractmethod
    async def update(cls, client: BaseRESTClient, obj: BaseModel, **kwargs) -> None: ...

    @classmethod
    @abstractmethod
    async def delete(cls, client: BaseRESTClient, pk: any, **kwargs) -> None:  ...

