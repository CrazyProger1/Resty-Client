from pydantic import BaseModel

from resty.types import BaseSerializer


class Serializer(BaseSerializer):
    @classmethod
    def serialize(cls, obj: BaseModel) -> dict:
        if not isinstance(obj, cls.schema):
            raise TypeError('Object must be of type {}'.format(cls.schema))
        return obj.model_dump()

    @classmethod
    def deserialize(cls, data: dict) -> BaseModel:
        return cls.schema.model_validate(data)
