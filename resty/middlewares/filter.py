from resty.requests import Request
from .types import BaseFilterMiddleware


class FilterMiddleware(BaseFilterMiddleware):
    async def handle_request(self, request: Request, **kwargs):
        pass
