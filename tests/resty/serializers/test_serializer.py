import pytest
from pydantic import BaseModel

from resty.enums import Endpoint
from resty.serializers import Serializer


class Schema1(BaseModel):
    id: int
    name: str
    private: bool


class CreateSchema(BaseModel):
    pass


class ReadSchema(BaseModel):
    pass


@pytest.mark.parametrize(
    "model, data", [(Schema1, {"id": 1, "name": "test", "private": True})]
)
def test_serializer_serialize(model, data):
    class Ser(Serializer):
        schema = model

    data = Ser.serialize(model(**data))

    assert data == data


@pytest.mark.parametrize(
    "model, data", [(Schema1, {"id": 1, "name": "test", "private": True})]
)
def test_serializer_deserialize(model, data):
    class Ser(Serializer):
        schema = model

    obj = Ser.deserialize(data)

    assert obj.model_dump() == data


@pytest.mark.parametrize(
    "model, data", [(Schema1, [{"id": 1, "name": "test", "private": True}])]
)
def test_serializer_deserialize_many(model, data):
    class Ser(Serializer):
        schema = model

    objects = Ser.deserialize_many(data)

    assert len(objects) == len(data)


@pytest.mark.parametrize(
    "models, context, expected_schema",
    [
        ({Endpoint.CREATE: CreateSchema}, {"endpoint": Endpoint.CREATE}, CreateSchema),
        ({Endpoint.READ: ReadSchema}, {"endpoint": Endpoint.READ}, ReadSchema),
        ({Endpoint.READ_ONE: Schema1}, {"endpoint": Endpoint.READ_ONE}, Schema1),
        ({Endpoint.BASE: Schema1}, {"endpoint": Endpoint.READ_ONE}, Schema1),
        ({Endpoint.BASE: Schema1}, {"schema": ReadSchema}, ReadSchema),
    ],
)
def test_get_schema(models, context, expected_schema):
    class Ser(Serializer):
        schemas = models

    assert Ser.get_schema(**context) == expected_schema


def test_get_unspecified_schema():
    class Ser(Serializer):
        pass

    with pytest.raises(TypeError):
        Ser.get_schema()
