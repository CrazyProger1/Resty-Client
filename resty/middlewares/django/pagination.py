from resty.middlewares.types import BasePaginationMiddleware
from resty.requests import Request
from resty.responses import Response


class DjangoPaginationMiddleware(BasePaginationMiddleware):
    def __init__(self, page_size: int = 100):
        self._page_size = page_size

    async def handle_request(self, request: Request, **kwargs):
        page = kwargs.get('page', 0)
        limit = self._page_size
        offset = page * limit
        request.params.update({
            'limit': limit,
            'offset': offset
        })

    async def handle_response(self, response: Response, **kwargs):
        results = response.data.get('results')
        response.data = results
