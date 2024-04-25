from dataclasses import dataclass, field

from resty.enums import Method


@dataclass
class Request:
    url: str
    method: Method
    data: dict = None
    json: dict = None
    timeout: int | None = None
    params: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    cookies: dict = field(default_factory=dict)
    redirects: bool = False
    middleware_options: dict = field(default_factory=dict)


@dataclass
class Response:
    request: Request
    status: int
    data: list | dict = None
    middleware_options: dict = field(default_factory=dict)
