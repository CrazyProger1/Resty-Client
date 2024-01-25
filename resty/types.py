from abc import ABC, abstractmethod

from typing import Iterable

from pydantic import BaseModel

from resty.enums import (
    Endpoint,
    Field
)
from resty.requests import Request
from resty.responses import Response


class BaseMiddleware(ABC):
    pass


class BasePreRequestMiddleware(BaseMiddleware):
    @abstractmethod
    async def handle_request(self, request: Request, **kwargs): ...


class BasePostRequestMiddleware(BaseMiddleware):
    @abstractmethod
    async def handle_response(self, response: Response, **kwargs): ...


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
    pk_field: str

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
