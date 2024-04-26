import asyncio

from resty.enums import Method
from resty.types import Request, Response
from resty.middlewares import BaseRequestMiddleware, BaseResponseMiddleware
from resty.clients.httpx import RESTClient


class LoggingMiddleware(BaseRequestMiddleware, BaseResponseMiddleware):
    async def __call__(self, reqresp: Request | Response, **kwargs):
        print(reqresp)


class HelloWorldMiddleware(BaseRequestMiddleware):

    async def __call__(self, request: Request, **kwargs):
        print('Hello, World!')


async def main():
    client = RESTClient()

    client.middlewares.add_middlewares(LoggingMiddleware())

    await client.request(Request(url="https://example.com", method=Method.GET))
    # Request(url='https://example.com', method=<Method.GET: 'GET'>, ...)
    # Response(request=Request(url='https://example.com', method=<Method.GET: 'GET'>, ...)

    with client.middlewares.middleware(HelloWorldMiddleware()):
        await client.request(Request(url="https://example.com", method=Method.GET))
        # Request(url='https://example.com', method=<Method.GET: 'GET'>, ...)
        # Hello, World!
        # Response(request=Request(url='https://example.com', method=<Method.GET: 'GET'>, ...)


if __name__ == "__main__":
    asyncio.run(main())
