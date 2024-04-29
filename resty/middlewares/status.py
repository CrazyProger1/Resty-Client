from typing import Container, Mapping

from resty.middlewares import BaseResponseMiddleware
from resty.types import Response
from resty.constants import STATUS_ERRORS
from resty.exceptions import HTTPError


class StatusCheckingMiddleware(BaseResponseMiddleware):
    def __init__(
        self,
        errors: Mapping[int, type[Exception]] = None,
        default_error: type[Exception] = HTTPError,
    ):
        self._errors = errors or STATUS_ERRORS
        self._default_error = default_error

    @staticmethod
    def _check_status(actual: int, expected: int | Container[int] = 200) -> bool:
        if isinstance(expected, Container):
            return actual in expected
        return actual == expected

    def _raise_error(self, status: int, *args):
        exc = self._errors.get(status, self._default_error)

        try:
            raise exc(*args)
        except TypeError:
            raise exc()

    async def __call__(self, response: Response, **kwargs):
        actual_status = response.status
        expected_status = kwargs.pop(
            "expected_status",
            {200, 201},
        )

        check_status = kwargs.pop("check_status", True)

        if check_status and not self._check_status(actual_status, expected_status):
            self._raise_error(actual_status, response)
