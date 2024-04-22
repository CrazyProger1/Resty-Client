from enum import Enum


class Endpoint(str, Enum):
    BASE = "base"
    CREATE = "create"
    READ = "read"
    READ_ONE = "read_one"
    UPDATE = "update"
    DELETE = "delete"


class Field(str, Enum):
    PRIMARY = "primary"


class Method(str, Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
