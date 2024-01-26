import asyncio
import httpx

from resty.clients.httpx import RESTClient
from resty.ext.django.middlewares import DjangoPagePaginationMiddleware

from managers import ProductManager


async def main():
    xclient = httpx.AsyncClient(base_url='http://localhost:8000/')
    rest_client = RESTClient(xclient=xclient)
    rest_client.add_middleware(DjangoPagePaginationMiddleware())
    for prod in await ProductManager.read(rest_client):
        print(prod)


if __name__ == '__main__':
    asyncio.run(main())
