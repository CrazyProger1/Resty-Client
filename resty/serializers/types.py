from abc import ABC, abstractmethod
from typing import Mapping, Iterable

from resty.types import Schema


class BaseSerializer(ABC):
    @classmethod
    @abstractmethod
    def serialize(
            cls,
            obj: Schema,
            **kwargs,
    ) -> Mapping: ...

    @classmethod
    @abstractmethod
    def serialize_many(
            cls,
            objs: Iterable[Schema],
            **kwargs,
    ) -> Iterable: ...

    @classmethod
    @abstractmethod
    def deserialize[T: Schema](
            cls,
            schema: type[T],
            data: Mapping,
            **kwargs,
    ) -> T: ...

    @classmethod
    @abstractmethod
    def deserialize_many[T: Schema](
            cls,
            schema: type[T],
            data: Iterable,
            **kwargs,
    ) -> Iterable[T]: ...
