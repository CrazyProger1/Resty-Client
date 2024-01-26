# RestyClient

<p align="center">
<img src="docs/resty-cat.png" alt="resty lib logo">
</p>

<a href="https://github.com/CrazyProger1/RestyClient/blob/master/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/CrazyProger1/Simple-XSS"></a>
<a href="https://github.com/CrazyProger1/RestyClient/releases/latest"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/CrazyProger1/RestyClient"></a>
<a href="https://pypi.org/project/resty-client/"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/resty-client"></a>
<a><img src="https://img.shields.io/pypi/status/resty-client"></a>

RestyClient is a simple, easy-to-use Python library for interacting with REST APIs using Pydantic's powerful data
validation and deserialization tools. This library provides an intuitive API that makes it easy to make HTTP requests
and handle data on the client side.

## Features

- Middleware system, which allows you to implement any pagination, filtering or authentication.

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

### Schema

```python
from pydantic import BaseModel


class Product(BaseModel):
    id: int | None = None
    name: str
    description: str
    code: str
```

### Serializer

```python
from resty.serializers import Serializer


class ProductSerializer(Serializer):
    schema = Product
```

### Manager

```python
from resty.enums import (
    Endpoint,
    Field
)
from resty.managers import Manager


class ProductManager(Manager):
    serializer = ProductSerializer
    endpoints = {
        Endpoint.CREATE: '/products/',
        Endpoint.READ: '/products/',
        Endpoint.READ_ONE: '/products/{pk}/',
        Endpoint.UPDATE: '/products/{pk}/',
        Endpoint.DELETE: '/products/{pk}/',
    }
    fields = {
        Field.PRIMARY: 'id',
    }
```

### CRUD

```python
from httpx import AsyncClient

from resty.clients.httpx import RESTClient


async def main():
    xclient = AsyncClient(base_url='http://localhost:8000/')
    rest_client = RESTClient(xclient=xclient)

    product = Product(
        name='First prod',
        description='My Desc',
        code='123W31Q'
    )

    # Create
    created = await ProductManager.create(rest_client, product)

    # Read
    my_product = await ProductManager.read_one(rest_client, created.id)

    for prod in await ProductManager.read(rest_client):
        print(prod.name)

    # Update
    my_product.description = 'QWERTY'
    await ProductManger.update(rest_client, my_product)

    # Delete
    await ProductManager.delete(rest_client, 1)
```

## Status

``0.0.1`` - INDEV

## Licence

RestyClient is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.