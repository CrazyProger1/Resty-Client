from abc import ABC

from resty.types import (
    BasePostRequestMiddleware,
    BasePreRequestMiddleware
)


class BasePaginationMiddleware(BasePreRequestMiddleware, BasePostRequestMiddleware, ABC):
    pass
