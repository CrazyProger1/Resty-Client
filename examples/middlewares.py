import asyncio

from resty.enums import Method
from resty.types import Request, Response
from resty.middlewares import BaseRequestMiddleware, BaseResponseMiddleware
from resty.clients.httpx import RESTClient


class LoggingMiddleware(BaseRequestMiddleware, BaseResponseMiddleware):
    async def __call__(self, reqresp: Request | Response, **kwargs):
        print(reqresp)


async def main():
    client = RESTClient()

    client.middlewares.add_middlewares(LoggingMiddleware())

    await client.request(Request(url="https://example.com", method=Method.GET))


if __name__ == "__main__":
    asyncio.run(main())
