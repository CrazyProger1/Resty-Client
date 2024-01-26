from dataclasses import (
    dataclass,
    field
)

from pydantic import BaseModel

from resty.enums import (
    Method
)


@dataclass
class Request:
    schema: type[BaseModel]
    url: str
    method: Method
    data: dict = None
    timeout: int = None
    params: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    cookies: dict[str, str] = field(default_factory=dict)
    redirects: bool = False
