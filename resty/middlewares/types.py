from abc import ABC

from resty.types import BaseResponseMiddleware, BaseRequestMiddleware


class BasePaginationMiddleware(BaseRequestMiddleware, BaseResponseMiddleware, ABC):
    pass


class BaseFilterMiddleware(BaseRequestMiddleware, ABC):
    pass
