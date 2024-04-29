# Resty-Client

<p align="center">
<img src="https://github.com/CrazyProger1/Resty-Client/blob/master/docs/resty-cat.png" alt="resty lib logo">
</p>

<p align="center">
<a href="https://github.com/CrazyProger1/Resty-Client/blob/master/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/CrazyProger1/Resty-Client"></a>
<a href="https://github.com/CrazyProger1/Resty-Client/releases/latest"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/CrazyProger1/Resty-Client"></a>
<a href="https://pypi.org/project/resty-client/"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/resty-client"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style"></a>
<img src="https://img.shields.io/badge/coverage-100%25-brightgreen" alt="Coverage"/>
</p>


Resty-Client is a simple, easy-to-use Python library for interacting with REST APIs using Pydantic's powerful data
validation and deserialization tools. This library provides an intuitive API that makes it easy to make HTTP requests
and handle data on the client side.

## Features

- Middleware system, which allows you to implement any pagination, filtering or authentication.
- Powerful data validation & deserialization using Pydantic
- Easy-to-Use

## Installation

Using pip:

```shell
pip install resty-client
```

Using Poetry:

```shell
poetry add resty-client
```

## Getting-Started

See [examples](examples) for more.

### Schemas

```python
from resty.types import Schema


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
```

### Manager

```python
from resty.managers import Manager
from resty.enums import Endpoint, Field


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
```

### CRUD

```python
import asyncio

import httpx

from resty.clients.httpx import RESTClient


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
        obj=UserUpdateSchema(id=1, username="admin123", ),
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
```

## Status

``0.0.5`` - **RELEASED**

## Licence

Resty-Client is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.