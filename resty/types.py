from dataclasses import dataclass, field

from pydantic import BaseModel

from resty.enums import Method, Endpoint

Schema = BaseModel


@dataclass
class Request:
    url: str
    method: Method
    endpoint: Endpoint = None
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
    content: bytes
    text: str
    json: list | dict
    middleware_options: dict = field(default_factory=dict)
