import httpx


class HTTPXAsyncClientMock(httpx.AsyncClient):  # pragma: nocover
    def __init__(self, response=None, error: Exception = None):
        self.response = response
        self.error = error
        super().__init__()

    async def request(self, *args, **kwargs):
        if self.error:
            raise self.error

        return self.response
