from resty.requests import Request
from resty.responses import Response
from .types import BasePaginationMiddleware


class PaginationMiddleware(BasePaginationMiddleware):
    async def handle_request(self, request: Request, **kwargs):
        pass

    async def handle_response(self, response: Response, **kwargs):
        pass
