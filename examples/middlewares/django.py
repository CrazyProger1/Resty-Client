import asyncio

import httpx

from resty.enums import Endpoint, Field
from resty.types import Schema
from resty.managers import Manager
from resty.clients.httpx import RESTClient
from resty.ext.django.middlewares.pagination import (
    LimitOffsetPaginationMiddleware,
    PagePaginationMiddleware,
)


class UserCreateSchema(Schema):
    username: str
    email: str
    password: str
    age: int


class UserReadSchema(Schema):
    id: int
    username: str
    email: str
    age: int


class UserUpdateSchema(Schema):
    username: str = None
    email: str = None


class UserManager(Manager):
    endpoints = {
        Endpoint.CREATE: "users/",
        Endpoint.READ: "users/",
        Endpoint.READ_ONE: "users/{pk}",
        Endpoint.UPDATE: "users/{pk}",
        Endpoint.DELETE: "users/{pk}",
    }
    fields = {
        Field.PRIMARY: "id",
    }


async def main():
    client = RESTClient(httpx.AsyncClient(base_url="https://localhost:8000"))

    # Using LimitOffset pagination middleware
    with client.middlewares.middleware(LimitOffsetPaginationMiddleware(limit=200)):
        manager = UserManager(client=client)

        paginated_response = await manager.read(
            response_type=UserReadSchema,
            offset=100,
        )

    # Using Page pagination middleware
    with client.middlewares.middleware(PagePaginationMiddleware()):
        manager = UserManager(client=client)

        paginated_response = await manager.read(
            response_type=UserReadSchema,
            page=3,
        )


if __name__ == "__main__":
    asyncio.run(main())
