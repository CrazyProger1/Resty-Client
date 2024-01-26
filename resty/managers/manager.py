from typing import Iterable

from pydantic import BaseModel

from resty.types import (
    BaseManager,
    BaseRESTClient
)
from resty.types import (
    Request
)
from resty.enums import (
    Endpoint,
    Method,
    Field
)


class Manager(BaseManager):
    @classmethod
    def _get_endpoint(cls, endpoint: Endpoint) -> str:
        return cls.endpoints.get(
            endpoint,
            cls.endpoints.get(
                endpoint.BASE,
                ''
            ))

    @classmethod
    def _get_pk_field(cls) -> str | None:
        return cls.fields.get(Field.PRIMARY)

    @classmethod
    async def create(cls, client: BaseRESTClient, obj: BaseModel, **kwargs) -> BaseModel:
        request = Request(
            schema=cls.serializer.schema,
            method=Method.POST,
            url=cls._get_endpoint(Endpoint.CREATE),
            data=cls.serializer.serialize(obj=obj)
        )
        response = await client.request(
            request=request,
            **kwargs
        )

        pk_field = cls._get_pk_field()
        pk = response.data.get(pk_field)
        setattr(obj, pk_field, pk)
        return obj

    @classmethod
    async def read(cls, client: BaseRESTClient, **kwargs) -> Iterable[BaseModel]:
        request = Request(
            schema=cls.serializer.schema,
            method=Method.GET,
            url=cls._get_endpoint(Endpoint.READ),
        )
        response = await client.request(
            request=request,
            **kwargs
        )
        result = []
        for dataset in response.data:
            result.append(cls.serializer.deserialize(dataset))
        return result

    @classmethod
    async def read_one(cls, client: BaseRESTClient, pk: any, **kwargs) -> BaseModel:
        request = Request(
            schema=cls.serializer.schema,
            method=Method.GET,
            url=cls._get_endpoint(Endpoint.READ_ONE).format(pk=pk),
        )
        response = await client.request(
            request=request,
            **kwargs
        )

        return cls.serializer.deserialize(response.data)

    @classmethod
    async def update(cls, client: BaseRESTClient, obj: BaseModel, **kwargs) -> None:
        pk_field = cls._get_pk_field()
        pk = getattr(obj, pk_field)

        data = cls.serializer.serialize(obj=obj)

        request = Request(
            schema=cls.serializer.schema,
            method=Method.PATCH,
            url=cls._get_endpoint(Endpoint.UPDATE).format(pk=pk),
            data=data
        )
        await client.request(
            request=request,
            **kwargs
        )

    @classmethod
    async def delete(cls, client: BaseRESTClient, pk: any, **kwargs) -> None:
        request = Request(
            schema=cls.serializer.schema,
            method=Method.DELETE,
            url=cls._get_endpoint(Endpoint.DELETE).format(pk=pk),
        )
        await client.request(
            request=request,
            **kwargs
        )
