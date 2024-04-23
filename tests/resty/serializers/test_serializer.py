import pytest
from pydantic import BaseModel

from resty.serializers import Serializer


class Schema1(BaseModel):
    id: int
    name: str
    private: bool


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

