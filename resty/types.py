from abc import ABC, abstractmethod
from typing import Iterable
from dataclasses import dataclass, field

from pydantic import BaseModel

from resty.enums import Endpoint, Field
from resty.enums import Method


@dataclass
class Request:
    url: str
    method: Method
    data: dict = None
    json: dict = None
    timeout: int | None = None
    params: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    cookies: dict = field(default_factory=dict)
    redirects: bool = False


@dataclass
class Response:
    request: Request
    status: int
    data: list | dict = None


class BaseMiddleware(ABC):
    pass


class BaseRequestMiddleware(BaseMiddleware):
    @abstractmethod
    async def handle_request(self, request: Request, **context): ...


class BaseResponseMiddleware(BaseMiddleware):
    @abstractmethod
    async def handle_response(self, response: Response, **context): ...


class BaseMiddlewareManager(ABC):
    @abstractmethod
    async def call_request_middlewares(self, request: Request, **context): ...

    @abstractmethod
    async def call_response_middlewares(self, response: Response, **context): ...

    @abstractmethod
    def add_middleware(self, middleware: BaseMiddleware): ...


class BaseRESTClient(ABC):
    @abstractmethod
    def add_middleware(self, middleware: BaseMiddleware): ...

    @abstractmethod
    async def request(self, request: Request, **context) -> Response: ...


class BaseSerializer:
    schema: type[BaseModel] = None
    schemas: dict[Endpoint, type[BaseModel]] = None

    @classmethod
    @abstractmethod
    def get_schema(cls, **context) -> type[BaseModel]: ...

    @classmethod
    @abstractmethod
    def serialize(cls, obj: BaseModel, **context) -> dict: ...

    @classmethod
    @abstractmethod
    def deserialize(cls, data: dict, **context) -> BaseModel: ...

    @classmethod
    @abstractmethod
    def deserialize_many(cls, data: list[dict], **context) -> list[BaseModel]: ...


class BaseManager:
    serializer: type[BaseSerializer] = None
    endpoints: dict[Endpoint, str] = {}
    fields: dict[Field, str] = {}

    @classmethod
    @abstractmethod
    async def create(
        cls, client: BaseRESTClient, obj: BaseModel, **kwargs
    ) -> BaseModel: ...

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
    async def delete(cls, client: BaseRESTClient, pk: any, **kwargs) -> None: ...
