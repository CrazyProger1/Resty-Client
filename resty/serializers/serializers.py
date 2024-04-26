from typing import Iterable, Mapping

from resty.serializers.types import BaseSerializer
from resty.types import Schema


class Serializer(BaseSerializer):
    @classmethod
    def serialize(cls, obj: Schema, **kwargs) -> Mapping:
        return obj.model_dump()

    @classmethod
    def serialize_many(cls, objs: Iterable[Schema], **kwargs) -> Iterable:
        return tuple(cls.serialize(obj=obj, **kwargs) for obj in objs)

    @classmethod
    def deserialize[T: Schema](cls, schema: type[T], data: Mapping, **kwargs) -> T:
        return schema.model_validate(data)

    @classmethod
    def deserialize_many[
    T: Schema
    ](cls, schema: type[T], data: Iterable, **kwargs, ) -> Iterable[T]:
        return tuple(cls.deserialize(schema=schema, data=dataset, **kwargs) for dataset in data)
