from resty.types import Schema
from resty.serializers import Serializer


def test_serialize():
    class MySchema(Schema):
        id: int
        name: str
        private: bool

    serializer = Serializer()

    obj = MySchema(id=1, name="test", private=False)

    assert serializer.serialize(obj) == obj.model_dump()


def test_serialize_many():
    class MySchema(Schema):
        id: int
        name: str
        private: bool

    serializer = Serializer()

    objs = [
        MySchema(id=1, name="test", private=False),
        MySchema(id=2, name="test2", private=True),
    ]

    assert serializer.serialize_many(objs) == tuple(obj.model_dump() for obj in objs)


def test_deserialize():
    class MySchema(Schema):
        id: int
        name: str
        private: bool

    serializer = Serializer()

    obj = MySchema(id=1, name="test", private=False)

    assert serializer.deserialize(MySchema, obj.model_dump()) == obj


def test_deserialize_many():
    class MySchema(Schema):
        id: int
        name: str
        private: bool

    serializer = Serializer()

    objs = (
        MySchema(id=1, name="test", private=False),
        MySchema(id=2, name="test2", private=True),
    )
    serialized = tuple(obj.model_dump() for obj in objs)

    assert serializer.deserialize_many(MySchema, serialized) == objs
