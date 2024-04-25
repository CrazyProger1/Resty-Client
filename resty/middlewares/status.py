from typing import Container

from resty.middlewares import BaseResponseMiddleware
from resty.types import Response
from resty.constants import STATUS_ERRORS
from resty.exceptions import HTTPError


class StatusCheckingMiddleware(BaseResponseMiddleware):
    async def __call__(self, response: Response, **kwargs):
        status = response.status
        expected_status = kwargs.pop('expected_status', 200)
        check_status = kwargs.pop('check_status', True)

        if check_status:
            if isinstance(status, Container):
                if status in expected_status:
                    return

            else:
                if status == expected_status:
                    return

        exc = STATUS_ERRORS.get(status, HTTPError)
        raise exc(response=response)
