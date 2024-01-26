import asyncio
import httpx

from resty.clients.httpx import RESTClient
from resty.requests import Request
from resty.enums import Method

from managers import ProductManager


async def main():
    xclient = httpx.AsyncClient(base_url='http://localhost:8000/')
    rest_client = RESTClient(xclient=xclient)

    prod = await ProductManager.read_one(rest_client, pk=3)
    print(prod)


if __name__ == '__main__':
    asyncio.run(main())
