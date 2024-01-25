from dataclasses import (
    dataclass,
    field
)
from resty.enums import (
    Method
)


@dataclass
class Request:
    url: str
    method: Method
    params: dict = field(default_factory=dict)
    data: dict = None
    headers: dict = field(default_factory=dict)
