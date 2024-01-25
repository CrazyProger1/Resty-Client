import asyncio
import httpx

from resty.clients.httpx import RESTClient
from resty.middlewares.django import DjangoPagePaginationMiddleware

from managers import ProductManager


async def main():
    xclient = httpx.AsyncClient(base_url='http://localhost:8000/')
    rest_client = RESTClient(xclient=xclient)
    rest_client.add_middleware(DjangoPagePaginationMiddleware())
    products = await ProductManager.read(rest_client, expected_status=200, page=1)
    for product in products:
        print(product)


if __name__ == '__main__':
    asyncio.run(main())


