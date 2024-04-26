from abc import ABC, abstractmethod
from typing import Mapping, Iterable

from resty.enums import Endpoint, Field, Method
from resty.types import Schema

type Endpoints = Mapping[Endpoint, str]
type Fields = Mapping[Field, str]
type Methods = Mapping[Endpoint, Method]


class BaseURLBuilder(ABC):
    @abstractmethod
    def build(self, endpoints: Endpoints, endpoint: Endpoint, **kwargs): ...


class BaseSerializer(ABC):

    @abstractmethod
    def serialize(self, obj: Schema, **kwargs) -> Mapping: ...

    @abstractmethod
    def serialize_many(self, objs: Iterable[Schema], **kwargs) -> Iterable: ...

    @abstractmethod
    def deserialize[T: Schema](self, schema: type[T], data: Mapping, **kwargs) -> T: ...

    @abstractmethod
    def deserialize_many[T: Schema](self, schema: type[T], data: Iterable, **kwargs) -> Iterable[T]: ...


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

    @abstractmethod
    async def create[T: Schema](self, obj: Schema | Mapping, response_schema: type[T] = None, **kwargs) -> T | None: ...

    @abstractmethod
    async def read[T: Schema](self, response_schema: type[T], **kwargs) -> Iterable[T]: ...

    @abstractmethod
    async def read_one[T: Schema](self, obj_or_pk: Schema | Mapping | any, response_schema: type[T], **kwargs) -> T: ...

    @abstractmethod
    async def update[T: Schema](self, obj: Schema | Mapping, response_schema: type[T] = None, **kwargs) -> T | None: ...

    @abstractmethod
    async def delete[T: Schema](self, obj_or_pk: Schema | Mapping | any, response_schema: type[T] = None,
                                **kwargs) -> T | None: ...
