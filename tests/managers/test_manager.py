import pytest

from resty.enums import Method, Endpoint, Field
from resty.managers import Manager
from resty.types import Response, Request, Schema

from tests.managers.conftest import RESTClientMock


class UserCreate(Schema):
    username: str


class UserRead(Schema):
    id: int
    username: str


class UserUpdate(Schema):
    id: int
    username: str


class UserManager(Manager):
    endpoints = {
        Endpoint.CREATE: "users/",
        Endpoint.READ: "users/",
        Endpoint.READ_ONE: "users/{pk}",
        Endpoint.UPDATE: "users/{pk}",
        Endpoint.DELETE: "users/{pk}",
    }
    fields = {
        Field.PRIMARY: "id",
    }


class UserManagerForURLBuilding(Manager):
    endpoints = {
        Endpoint.READ_ONE: "users/{pk}/{abc}",
    }
    fields = {
        Field.PRIMARY: "id",
    }


class ManagerWithoutSerializer(Manager):
    serializer_class = None


class ManagerWithInvalidSerializer(Manager):
    serializer_class = 123


class ManagerWithUnspecifiedMethods(Manager):
    methods = {}


class ManagerWithUnspecifiedFields(Manager):
    pass


class ManagerWithPkField(Manager):
    fields = {
        Field.PRIMARY: "id",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client, obj",
    [
        (
            RESTClientMock(json={"username": "test"}, method=Method.POST),
            UserCreate(username="test"),
        ),
        (
            RESTClientMock(json={"username": "321"}, method=Method.POST),
            UserCreate(username="321"),
        ),
        (
            RESTClientMock(json={"username": "test"}, method=Method.POST),
            {"username": "test"},
        ),
    ],
)
async def test_create(client, obj):
    manager = UserManager()

    await manager.create(client=client, obj=obj)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        (
            {"username": "test", "id": 1},
            {"username": "test123", "id": 2},
            {"username": "test321", "id": 3},
        ),
    ],
)
async def test_read(data):
    client = RESTClientMock(
        response=Response(
            request=Request(url="", method=Method.GET),
            status=200,
            json=data,
        ),
        method=Method.GET,
    )
    manager = UserManager()

    objs = await manager.read(client=client, response_type=UserRead)

    assert tuple(obj.model_dump() for obj in objs) == data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client, obj",
    [
        (
            RESTClientMock(
                response=Response(
                    Request("", Method.GET),
                    status=200,
                    json={"username": "test", "id": 123},
                ),
                method=Method.GET,
            ),
            UserRead(username="test", id=123),
        ),
    ],
)
async def test_read_one(client, obj):
    manager = UserManager()

    assert (
        await manager.read_one(client=client, obj_or_pk=123, response_type=UserRead)
        == obj
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client, obj",
    [
        (
            RESTClientMock(
                response=Response(
                    Request("", Method.GET),
                    status=200,
                    json={"username": "test", "id": 123},
                ),
                method=Method.PATCH,
                url="users/123",
            ),
            UserUpdate(username="test", id=123),
        ),
    ],
)
async def test_update(client, obj):
    manager = UserManager()

    await manager.update(client=client, obj=obj)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client, pk",
    [
        (RESTClientMock(url="users/123", method=Method.DELETE), 123),
        (
            RESTClientMock(url="users/321", method=Method.DELETE),
            UserRead(username="test", id=321),
        ),
    ],
)
async def test_delete(client, pk):
    manager = UserManager()

    await manager.delete(obj_or_pk=pk, client=client)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client, pk, abc",
    [
        (RESTClientMock(url="users/123/hello"), 123, "hello"),
        (RESTClientMock(url="users/321/world"), 321, "world"),
    ],
)
async def test_url_building(client, pk, abc):
    manager = UserManagerForURLBuilding()

    await manager.read_one(client=client, obj_or_pk=pk, abc=abc)


@pytest.mark.parametrize(
    "manager",
    [
        ManagerWithoutSerializer,
        ManagerWithInvalidSerializer,
    ],
)
def test_invalid_or_unspec_serializer(manager):
    manager = manager()

    with pytest.raises(RuntimeError):
        manager.get_serializer()


def test_get_unspec_method():
    manager = ManagerWithUnspecifiedMethods()

    with pytest.raises(RuntimeError):
        manager.get_method(Endpoint.CREATE)


def test_get_unspec_field():
    manager = ManagerWithUnspecifiedFields()

    with pytest.raises(RuntimeError):
        manager.get_field(Field.PRIMARY)


def test_get_field():
    manager = ManagerWithPkField()

    assert manager.get_field(Field.PRIMARY) == "id"


@pytest.mark.parametrize(
    "obj, pk",
    [
        ({"id": "test"}, "test"),
        (UserRead(id=321, username="123"), 321),
    ],
)
def test_get_pk(obj, pk):
    manager = ManagerWithPkField()

    assert manager.get_pk(obj) == pk


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url",
    [
        "test",
    ],
)
async def test_passing_url(url):
    client = RESTClientMock(url=url)
    manager = UserManagerForURLBuilding(client=client)

    await manager.delete(obj_or_pk=1, url=url)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, response_type, result",
    [
        ({"username": "test"}, dict, {"username": "test"}),
        (("username", "test"), list, ["username", "test"]),
        (
            {"username": "test", "id": 123},
            lambda r: dict.keys(r.json),
            dict.keys({"username": "test", "id": 123}),
        ),
        (
            {"username": "test", "id": 123},
            lambda r, t: dict.keys(r),
            {"username": "test", "id": 123},
        ),
    ],
)
async def test_response_type(data, response_type, result):
    client = RESTClientMock(
        response=Response(
            request=Request(
                url="",
                method=Method.GET,
            ),
            status=200,
            json=data,
        )
    )

    manager = UserManager()

    response = await manager.read(
        client=client,
        response_type=response_type,
    )

    assert response == result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "client",
    [
        None,
        "test",
    ],
)
async def test_passing_invalid_client(client):
    manager = UserManager()

    with pytest.raises(TypeError):
        await manager.read(client=client)
