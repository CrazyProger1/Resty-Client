from abc import ABC, abstractmethod
from typing import Mapping, Iterable, Callable

from resty.enums import Endpoint, Field, Method
from resty.serializers import BaseSerializer
from resty.clients import BaseRESTClient
from resty.types import Schema, Response

type Endpoints = Mapping[Endpoint, str]
type Fields = Mapping[Field, str]
type Methods = Mapping[Endpoint, Method]
type ResponseType = type[Schema] | type[Mapping | Iterable] | Callable[[Response, ], any] | None


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

    @abstractmethod
    def get_serializer(self, **kwargs) -> type[BaseSerializer]: ...

    @abstractmethod
    def get_method(self, endpoint: Endpoint, **kwargs) -> Method: ...

    @abstractmethod
    def get_field(self, field: Field) -> str: ...

    @abstractmethod
    def get_pk(self, obj: Schema | Mapping) -> any: ...

    @abstractmethod
    async def create[T: Schema](
            self,
            obj: Schema | Mapping,
            response_type: ResponseType = None,
            **kwargs,
    ) -> T | None: ...

    @abstractmethod
    async def read[T: Schema](
            self,
            response_type: ResponseType = None,
            **kwargs,
    ) -> Iterable[T]: ...

    @abstractmethod
    async def read_one[T: Schema](
            self,
            obj_or_pk: Schema | Mapping | any,
            response_type: ResponseType = None,
            **kwargs,
    ) -> T: ...

    @abstractmethod
    async def update[T: Schema](
            self,
            obj: Schema | Mapping,
            response_type: ResponseType = None,
            **kwargs,
    ) -> T | None: ...

    @abstractmethod
    async def delete[T: Schema](
            self,
            obj_or_pk: Schema | Mapping | any,
            response_type: ResponseType = None,
            **kwargs,
    ) -> T | None: ...
