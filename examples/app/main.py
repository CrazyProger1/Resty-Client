import asyncio
import httpx

from resty.clients.httpx import RESTClient
from resty.middlewares.django import DjangoPaginationMiddleware

from managers import ProductManager


async def main():
    xclient = httpx.AsyncClient(base_url='http://localhost:8000/')
    rest_client = RESTClient(xclient=xclient)
    rest_client.add_middleware(DjangoPaginationMiddleware(page_size=100))
    result = await ProductManager.read(rest_client)


if __name__ == '__main__':
    asyncio.run(main())
