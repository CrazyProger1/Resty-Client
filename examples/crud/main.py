import asyncio
import httpx

from resty.clients.httpx import RESTClient
from resty.ext.django.middlewares import DjangoPagePaginationMiddleware

from managers import ProductManager
from schemas import ProductSchema


async def main():
    xclient = httpx.AsyncClient(base_url='http://localhost:8000/')

    rest_client = RESTClient(xclient=xclient)

    rest_client.add_middleware(DjangoPagePaginationMiddleware())

    product = ProductSchema(
        name='My Product',
        description='My Desc',
        code='123W31QQW'
    )

    # Create
    created = await ProductManager.create(rest_client, product)

    # Read
    my_product = await ProductManager.read_one(rest_client, created.id)

    for prod in await ProductManager.read(rest_client):
        print(prod.name)

    # Update
    my_product.description = 'QWERTY'
    await ProductManager.update(rest_client, my_product)

    # Delete
    await ProductManager.delete(rest_client, my_product.id)


if __name__ == '__main__':
    asyncio.run(main())
