from resty.middlewares import BasePaginationMiddleware
from resty.types import (
    Response,
    Request
)
from resty.enums import (
    Method
)


class DjangoPagePaginationMiddleware(BasePaginationMiddleware):
    async def handle_request(self, request: Request, **kwargs):
        if request.method in {Method.GET, }:
            page = kwargs.pop('page', 1)

            request.params.update({
                'page': page,
            })

    async def handle_response(self, response: Response, **kwargs):
        if response.request.method in {Method.GET, }:
            data = response.data
            results = data.get('results', data)
            response.data = results


class DjangoLimitOffsetPaginationMiddleware(DjangoPagePaginationMiddleware):
    def __init__(self, page_size: int = 100):
        self._limit = page_size

    async def handle_request(self, request: Request, **kwargs):
        if request.method in {Method.GET, }:
            page = kwargs.pop('page', 1) - 1
            limit = kwargs.pop('limit', self._limit)
            offset = kwargs.pop('offset', page * self._limit)

            request.params.update({
                'limit': limit,
                'offset': offset
            })
