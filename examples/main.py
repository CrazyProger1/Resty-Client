import asyncio
from abc import ABC, abstractmethod

from dataclasses import dataclass, field
from typing import Callable, Iterable

from httpx import AsyncClient
from pydantic import BaseModel


class BaseMiddleware(ABC):
    pass


class BaseFilter(ABC):
    pass


@dataclass
class Request:
    schema: type[BaseModel]
    url: str
    method: str
    params: dict = field(default_factory=dict)
    data: dict = None
    headers: dict = None


@dataclass
class Response:
    schema: type[BaseModel]
    request: Request
    status: int
    data: dict = None


class BaseClient(ABC):
    @abstractmethod
    def add_middleware(self, middleware: BaseMiddleware): ...

    @abstractmethod
    async def request(self, request: Request, **kwargs) -> Response: ...


class HTTPXClient(BaseClient):
    def __init__(self, xclient: AsyncClient, default_middlewares: Iterable[BaseMiddleware] = None):
        self._xclient = xclient
        self._middlewares = list(default_middlewares) if default_middlewares else []

    def add_middleware(self, middleware: BaseMiddleware):
        self._middlewares.append(middleware)

    async def _call_pre_middlewares(self, request: Request, **kwargs):
        for middleware in self._middlewares:
            if isinstance(middleware, BasePreRequestMiddleware):
                await middleware.handle_request(request=request, **kwargs)

    async def _call_post_middlewares(self, response: Response):
        pass

    async def request(self, request: Request, **kwargs) -> Response:
        await self._call_pre_middlewares(request=request, **kwargs)
        response = await self._xclient.request(
            method=request.method,
            url=request.url,
            data=request.data,
            params=request.params,
            headers=request.headers
        )

        print(response.json())


class BaseSerializer:
    schema: type[BaseModel]

    @classmethod
    @abstractmethod
    def serialize(cls, obj: BaseModel) -> dict: ...

    @classmethod
    @abstractmethod
    def deserialize(cls, data: dict) -> BaseModel: ...


class Serializer(BaseSerializer):
    @classmethod
    def serialize(cls, obj: BaseModel) -> dict:
        return obj.model_dump()

    @classmethod
    def deserialize(cls, data: dict) -> BaseModel:
        return cls.schema.model_validate(data)


class BaseManager:
    schema: type[BaseModel]
    endpoints: dict
    authable: bool = False
    auth_fields: dict
    pk_field: str

    @classmethod
    @abstractmethod
    async def create(cls, client: BaseClient, obj: BaseModel, **kwargs) -> BaseModel: ...

    @classmethod
    @abstractmethod
    async def read(cls, client: BaseClient, **kwargs) -> Iterable[BaseModel]: ...

    @classmethod
    @abstractmethod
    async def read_one(cls, client: BaseClient, pk: any, **kwargs) -> BaseModel: ...

    @classmethod
    @abstractmethod
    async def update(cls, client: BaseClient, obj: BaseModel, **kwargs) -> None: ...

    @classmethod
    @abstractmethod
    async def delete(cls, client: BaseClient, pk: any, **kwargs) -> None:  ...


class Manager(BaseManager):
    @classmethod
    async def create(cls, client: BaseClient, obj: BaseModel, **kwargs) -> BaseModel:
        request = Request(
            schema=cls.schema,
            url=cls.endpoints.get('create'),
            method='POST',
            data=Serializer.serialize(obj)
        )
        response = await client.request(
            request=request,
            **kwargs
        )

    @classmethod
    async def read(cls, client: BaseClient, **kwargs) -> Iterable[BaseModel]:
        request = Request(
            schema=cls.schema,
            url=cls.endpoints.get('read'),
            method='GET'
        )
        response = await client.request(
            request=request,
            **kwargs
        )

    @classmethod
    async def read_one(cls, client: BaseClient, pk: any, **kwargs) -> BaseModel:
        pass

    @classmethod
    async def update(cls, client: BaseClient, obj: BaseModel, **kwargs) -> None:
        pass

    @classmethod
    async def delete(cls, client: BaseClient, pk: any, **kwargs) -> None:
        pass


class BasePreRequestMiddleware(BaseMiddleware):
    async def handle_request(self, request: Request, **kwargs): ...


class BasePostRequestMiddleware(BaseMiddleware):
    async def handle_response(self, response: Response, **kwargs): ...


class AuthMiddleware(BaseMiddleware):
    pass


class PaginationMiddleware(BasePreRequestMiddleware, BasePostRequestMiddleware, ABC):
    @abstractmethod
    async def handle_request(self, request: Request, **kwargs): ...


class FilterMiddleware(BaseMiddleware):
    pass


class DjangoPaginationMiddleware(PaginationMiddleware):
    def __init__(self, page_size: int = 10):
        self._page_size = page_size

    async def handle_request(self, request: Request, **kwargs):
        page = kwargs.get('page', 0)
        limit = self._page_size
        offset = page * limit
        request.params.update({
            'limit': limit,
            'offset': offset
        })

    async def handle_response(self, response: Response, **kwargs):
        results = response.data.get('results')
        response.data = results


class Product(BaseModel):
    id: int | None = None
    name: str
    description: str
    code: str


class ProductSerializer(Serializer):
    schema = Product


class ProductManager(Manager):
    schema = Product
    endpoints = {
        'create': '/products/',
        'read': '/products/',
        'read_one': '/products/{pk}/',
        'update': '/products/{pk}/',
        'delete': '/products/{pk}/'
    }
    pk_field = 'id'


async def main():
    async with AsyncClient(base_url='http://localhost:8000/') as xclient:
        client = HTTPXClient(
            xclient=xclient,
            default_middlewares=(
                DjangoPaginationMiddleware(page_size=100),
            ))
        products = await ProductManager.read(client=client)


if __name__ == '__main__':
    asyncio.run(main())
