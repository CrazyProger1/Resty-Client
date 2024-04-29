import asyncio

import httpx

from resty.enums import Endpoint, Field
from resty.types import Schema
from resty.managers import Manager
from resty.clients.httpx import RESTClient


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

    manager = UserManager()

    response = await manager.create(
        client=client,
        obj=UserCreateSchema(
            username="admin",
            email="admin@admin.com",
            password="admin",
            age=19,
        ),
        response_type=UserReadSchema,
    )
    print(response)  # id=1 username='admin' email='admin@admin.com' age=19

    response = await manager.read(
        client=client,
        response_type=UserReadSchema,
    )

    for obj in response:
        print(obj)  # id=1 username='admin' email='admin@admin.com' age=19

    response = await manager.read_one(
        client=client,
        obj_or_pk=1,
        response_type=UserReadSchema,
    )

    print(response)  # id=1 username='admin' email='admin@admin.com' age=19

    response = await manager.update(
        client=client,
        obj=UserUpdateSchema(
            id=1,
            username="admin123",
        ),
        response_type=UserReadSchema,
    )

    print(response)  # id=1 username='admin123' email='admin@admin.com' age=19

    await manager.delete(
        client=client,
        obj_or_pk=1,
        expected_status=204,
    )


if __name__ == "__main__":
    asyncio.run(main())
