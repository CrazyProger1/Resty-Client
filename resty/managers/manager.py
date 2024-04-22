from typing import Iterable

from pydantic import BaseModel

from resty.types import BaseManager, BaseRESTClient
from resty.types import Request
from resty.enums import Endpoint, Method, Field


class Manager(BaseManager):
    @classmethod
    def _get_endpoint(cls, endpoint: Endpoint) -> str:
        return cls.endpoints.get(endpoint, cls.endpoints.get(endpoint.BASE, ""))

    @classmethod
    def _get_pk_field(cls) -> str | None:
        return cls.fields.get(Field.PRIMARY)

    @classmethod
    def _get_request_kwargs(
            cls, method: Method, url: str, json: dict = None, kwargs: dict = None
    ) -> dict:
        return {
            "method": method,
            "url": kwargs.pop("url", url),
            "json": json,
            "headers": kwargs.pop("headers", {}),
            "params": kwargs.pop("params", {}),
            "cookies": kwargs.pop("cookies", {}),
            "redirects": kwargs.pop("redirects", False),
            "timeout": kwargs.pop("timeout", None),
        }

    @classmethod
    async def create(
            cls, client: BaseRESTClient, obj: BaseModel, **kwargs
    ) -> BaseModel:
        set_pk = kwargs.pop("set_pk", True)

        request = Request(
            **cls._get_request_kwargs(
                method=Method.POST,
                url=cls._get_endpoint(Endpoint.CREATE),
                json=cls.serializer.serialize(obj=obj, endpoint=Endpoint.CREATE),
                kwargs=kwargs,
            ),
        )

        response = await client.request(request=request, **kwargs)

        if set_pk:
            pk_field = cls._get_pk_field()
            pk = response.data.get(pk_field)
            setattr(obj, pk_field, pk)

        return obj

    @classmethod
    async def read(cls, client: BaseRESTClient, **kwargs) -> Iterable[BaseModel]:
        request = Request(
            **cls._get_request_kwargs(
                method=Method.GET,
                url=cls._get_endpoint(Endpoint.READ),
                kwargs=kwargs
            )
        )
        response = await client.request(request=request, **kwargs)
        result = []
        for dataset in response.data:
            result.append(cls.serializer.deserialize(dataset, endpoint=Endpoint.READ))
        return result

    @classmethod
    async def read_one(cls, client: BaseRESTClient, pk: any, **kwargs) -> BaseModel:
        request = Request(
            **cls._get_request_kwargs(
                method=Method.GET,
                url=cls._get_endpoint(Endpoint.READ_ONE).format(pk=pk),
                kwargs=kwargs,
            )
        )
        response = await client.request(request=request, **kwargs)

        return cls.serializer.deserialize(response.data, endpoint=Endpoint.READ_ONE)

    @classmethod
    async def update(cls, client: BaseRESTClient, obj: BaseModel, **kwargs) -> None:
        pk_field = cls._get_pk_field()
        pk = getattr(obj, pk_field)

        data = cls.serializer.serialize(obj=obj, endpoint=Endpoint.UPDATE)

        request = Request(
            **cls._get_request_kwargs(
                method=Method.PATCH,
                url=cls._get_endpoint(Endpoint.UPDATE).format(pk=pk),
                json=data,
                kwargs=kwargs,
            )
        )
        await client.request(request=request, **kwargs)

    @classmethod
    async def delete(cls, client: BaseRESTClient, pk: any, **kwargs) -> None:
        request = Request(
            **cls._get_request_kwargs(
                method=Method.DELETE,
                url=cls._get_endpoint(Endpoint.DELETE).format(pk=pk),
                kwargs=kwargs,
            )
        )
        await client.request(request=request, **kwargs)
