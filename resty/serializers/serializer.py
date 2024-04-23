import inspect

from pydantic import BaseModel

from resty.types import BaseSerializer


class Serializer(BaseSerializer):

    @classmethod
    def get_schema(cls, **context) -> type[BaseModel]:
        schema = context.get("schema")

        if inspect.isclass(schema) and issubclass(schema, BaseModel):
            return schema

        endpoint = context.get("endpoint")
        schema = cls.schema

        if cls.schemas is not None:
            schema = cls.schemas.get(endpoint, cls.schema)

        if schema is None:
            raise TypeError(f"Schema should be specified for {endpoint}")

        return schema

    @classmethod
    def serialize(cls, obj: BaseModel, **context) -> dict:
        schema = cls.get_schema(**context)
        if not isinstance(obj, schema):
            raise TypeError("Object must be of type {}".format(schema))
        return obj.model_dump()

    @classmethod
    def deserialize(cls, data: dict, **context) -> BaseModel:
        schema = cls.get_schema(**context)
        return schema.model_validate(data)

    @classmethod
    def deserialize_many(cls, data: list[dict], **context) -> list[BaseModel]:
        return [cls.deserialize(dataset, **context) for dataset in data]
