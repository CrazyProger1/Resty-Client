from abc import ABC, abstractmethod
from typing import Mapping, Iterable

from resty.enums import Endpoint, Field, Method
from resty.serializers import BaseSerializer
from resty.types import Schema

type Endpoints = Mapping[Endpoint, str]
type Fields = Mapping[Field, str]
type Methods = Mapping[Endpoint, Method]


class BaseURLBuilder(ABC):
    @classmethod
    @abstractmethod
    def build(
            cls,
            base: str,
            endpoints: Endpoints,
            endpoint: Endpoint,
            **kwargs,
    ) -> str: ...


class BaseManager(ABC):
    url: str = None
    methods: Methods = {
        Endpoint.CREATE: Method.POST,
        Endpoint.READ: Method.GET,
        Endpoint.READ_ONE: Method.GET,
        Endpoint.UPDATE: Method.PATCH,
        Endpoint.DELETE: Method.DELETE,
    }
    endpoints: Endpoints = {}
    fields: Fields = {}
    serializer_class: BaseSerializer
    url_builder_class: BaseURLBuilder

    @classmethod
    @abstractmethod
    async def create[T: Schema](
            cls,
            obj: Schema | Mapping,
            response_schema: type[T] = None,
            **kwargs,
    ) -> T | None: ...

    @classmethod
    @abstractmethod
    async def read[T: Schema](
            cls,
            response_schema: type[T],
            **kwargs,
    ) -> Iterable[T]: ...

    @classmethod
    @abstractmethod
    async def read_one[T: Schema](
            cls,
            obj_or_pk: Schema | Mapping | any,
            response_schema: type[T],
            **kwargs,
    ) -> T: ...

    @classmethod
    @abstractmethod
    async def update[T: Schema](
            cls,
            obj: Schema | Mapping,
            response_schema: type[T] = None,
            **kwargs,
    ) -> T | None: ...

    @classmethod
    @abstractmethod
    async def delete[T: Schema](
            cls,
            obj_or_pk: Schema | Mapping | any,
            response_schema: type[T] = None,
            **kwargs,
    ) -> T | None: ...
