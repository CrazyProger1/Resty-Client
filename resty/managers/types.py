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

    @classmethod
    @abstractmethod
    def get_serializer(cls, **kwargs) -> type[BaseSerializer]: ...

    @classmethod
    @abstractmethod
    def get_method(cls, endpoint: Endpoint, **kwargs) -> Method: ...

    @classmethod
    @abstractmethod
    def get_field(cls, field: Field) -> str: ...

    @classmethod
    @abstractmethod
    def get_pk(cls, obj: Schema | Mapping) -> any: ...

    @classmethod
    @abstractmethod
    async def create[T: Schema](
            cls,
            client: BaseRESTClient,
            obj: Schema | Mapping,
            response_type: ResponseType = None,
            **kwargs,
    ) -> T | None: ...

    @classmethod
    @abstractmethod
    async def read[T: Schema](
            cls,
            client: BaseRESTClient,
            response_type: ResponseType = None,
            **kwargs,
    ) -> Iterable[T]: ...

    @classmethod
    @abstractmethod
    async def read_one[T: Schema](
            cls,
            client: BaseRESTClient,
            obj_or_pk: Schema | Mapping | any,
            response_type: ResponseType = None,
            **kwargs,
    ) -> T: ...

    @classmethod
    @abstractmethod
    async def update[T: Schema](
            cls,
            client: BaseRESTClient,
            obj: Schema | Mapping,
            response_type: ResponseType = None,
            **kwargs,
    ) -> T | None: ...

    @classmethod
    @abstractmethod
    async def delete[T: Schema](
            cls,
            client: BaseRESTClient,
            obj_or_pk: Schema | Mapping | any,
            response_type: ResponseType = None,
            **kwargs,
    ) -> T | None: ...
