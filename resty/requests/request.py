from dataclasses import (
    dataclass,
    field
)


@dataclass
class Request:
    url: str
    method: str
    params: dict = field(default_factory=dict)
    data: dict = None
    headers: dict = field(default_factory=dict)
