import asyncio
import httpx

from resty.clients.httpx import RESTClient

from managers import ProductManager


async def main():
    xclient = httpx.AsyncClient(base_url='http://localhost:8000/')
    rest_client = RESTClient(xclient=xclient)

    await ProductManager.delete(rest_client, 1)


if __name__ == '__main__':
    asyncio.run(main())
