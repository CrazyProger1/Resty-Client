from dataclasses import dataclass

from resty.requests import Request


@dataclass
class Response:
    request: Request
    status: int
    data: dict = None
