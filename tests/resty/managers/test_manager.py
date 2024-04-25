import pytest
from pydantic import BaseModel

from resty.enums import Field, Endpoint, Method
from resty.exceptions import URLFormattingError
from resty.managers import Manager
from resty.serializers import Serializer
from conftest import MockRESTClient


class UserSchema(BaseModel):
    id: int = None
    username: str


class UserSerializer(Serializer):
    schema = UserSchema


class UserManager(Manager):
    serializer = UserSerializer

    endpoints = {
        Endpoint.CREATE: "users/",
        Endpoint.READ: "users/",
        Endpoint.READ_ONE: "users/{pk}",
        Endpoint.UPDATE: "users/{pk}",
        Endpoint.DELETE: "users/{pk}",
    }

    fields = {Field.PRIMARY: "id"}


class ManagerWithUnspecifiedEndpoints(Manager):
    pass


class ManagerWithUnspecifiedSerializer(Manager):
    endpoints = {
        Endpoint.CREATE: "users/",
        Endpoint.READ: "users/",
        Endpoint.READ_ONE: "users/{pk}",
        Endpoint.UPDATE: "users/{pk}",
        Endpoint.DELETE: "users/{pk}",
    }


class ManagerWithUnspecifiedFields(ManagerWithUnspecifiedSerializer):
    serializer = UserSerializer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, status, data, pk",
    [
        ("users/", 200, {"username": "test"}, 123),
        ("users/", 200, {"username": "superadmin"}, 321),
    ],
)
async def test_manager_create(url, status, data, pk):
    obj = await UserManager.create(
        MockRESTClient(
            expected_url=url,
            status=status,
            data={**data, "id": pk},
            expected_method=Method.POST,
            expected_json={**data, "id": None},
        ),
        UserSchema(**data),
    )

    assert obj.model_dump() == {**data, "id": pk}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, status, data",
    [
        (
                "users/",
                200,
                [
                    {"username": "test", "id": 123},
                    {"username": "ttt", "id": 321},
                    {"username": "321", "id": 4321},
                ],
        )
    ],
)
async def test_manager_read(url, status, data):
    objs = await UserManager.read(
        MockRESTClient(
            expected_url=url, status=status, data=data, expected_method=Method.GET
        ),
    )

    for obj, dataset in zip(objs, data):
        assert obj.model_dump() == dataset


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, status, data, pk",
    [
        ("users/123", 200, {"username": "test", "id": 123}, 123),
        ("users/333", 200, {"username": "test2", "id": 333}, 333),
    ],
)
async def test_manager_read_one(url, status, data, pk):
    obj = await UserManager.read_one(
        MockRESTClient(
            expected_url=url, status=status, data=data, expected_method=Method.GET
        ),
        pk=pk,
    )
    assert obj.model_dump() == data
    assert obj.id == pk


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, status, data, pk",
    [
        ("users/123", 200, {"username": "test", "id": 123}, 123),
        ("users/333", 200, {"username": "test2", "id": 333}, 333),
    ],
)
async def test_manager_update(url, status, data, pk):
    await UserManager.update(
        MockRESTClient(
            expected_url=url,
            status=status,
            data=data,
            expected_method=Method.PATCH,
            expected_json=data,
        ),
        obj=UserSchema(**data),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url, status, pk",
    [
        ("users/123", 200, 123),
        ("users/333", 200, 333),
    ],
)
async def test_manager_delete(url, status, pk):
    await UserManager.delete(
        MockRESTClient(
            expected_url=url, status=status, expected_method=Method.DELETE, data={}
        ),
        pk=pk,
    )


@pytest.mark.asyncio
async def test_unspecified_endpoint():
    with pytest.raises(RuntimeError):
        await ManagerWithUnspecifiedEndpoints.delete(
            MockRESTClient(),
            1
        )


@pytest.mark.asyncio
async def test_unspecified_serializer():
    with pytest.raises(RuntimeError):
        await ManagerWithUnspecifiedSerializer.create(
            MockRESTClient(),
            UserSchema(username='hello')
        )


@pytest.mark.asyncio
async def test_unspecified_field():
    with pytest.raises(RuntimeError):
        await ManagerWithUnspecifiedFields.create(
            MockRESTClient(),
            UserSchema(username='hello')
        )


@pytest.mark.asyncio
async def test_url_priority():
    await UserManager.delete(MockRESTClient(expected_url='https://test.com'), pk=1, url='https://test.com')


@pytest.mark.asyncio
async def test_url_injecting():
    await UserManager.delete(MockRESTClient(expected_url='/123'), pk=1, abc=123, url='/{abc}')


@pytest.mark.asyncio
async def test_url_not_injected():
    with pytest.raises(URLFormattingError):
        await UserManager.delete(MockRESTClient(expected_url='/123'), pk=1, url='/{abc}')
