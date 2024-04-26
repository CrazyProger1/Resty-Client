import asyncio

from resty.enums import Method
from resty.types import Request
from resty.clients.httpx import RESTClient


async def main():
    client = RESTClient()

    response = await client.request(
        Request(url="https://example.com", method=Method.GET)
    )

    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
