import inspect
from typing import Iterable

from pydantic import BaseModel

from resty.types import BaseManager, BaseRESTClient, Request, BaseSerializer
from resty.enums import Endpoint, Method, Field
from resty.exceptions import URLFormattingError


class Manager(BaseManager):
    @classmethod
    def _get_endpoint_url(cls, endpoint: Endpoint) -> str:
        url = cls.endpoints.get(endpoint, cls.endpoints.get(endpoint.BASE, None))
        if url is None:
            raise RuntimeError(
                f"Endpoint.{endpoint.name} and Endpoint.BASE not specified at endpoints"
            )
        return url

    @classmethod
    def _get_pk_field(cls) -> str | None:
        field = cls.fields.get(Field.PRIMARY)
        if field is None:
            raise RuntimeError("Field.PRIMARY not specified at fields")
        return field

    @classmethod
    def _get_pk(cls, obj) -> any:
        pk_field = cls._get_pk_field()
        if isinstance(obj, dict):
            return obj.get(pk_field)
        return getattr(obj, pk_field)

    @classmethod
    def _set_pk(cls, obj: BaseModel, pk: any):
        setattr(obj, cls._get_pk_field(), pk)

    @classmethod
    def _inject_into_url(cls, url: str, **data) -> str:
        try:
            return url.format(**data)
        except KeyError as e:
            raise URLFormattingError(f"Missing '{e.args[0]}' in {url}")

    @classmethod
    def _prepare_url(cls, **options) -> str:
        url = options.get("url")

        if url is not None:
            return url

        endpoint = options.get("endpoint", Endpoint.BASE)
        url = cls._get_endpoint_url(endpoint)
        return cls._inject_into_url(url, **options)

    @classmethod
    def _build_request(cls, **options) -> Request:
        return Request(
            method=options.get("method", Method.GET),
            url=options.get("url"),
            json=options.get("json", {}),
            headers=options.get("headers", {}),
            params=options.get("params", {}),
            cookies=options.get("cookies", {}),
            redirects=options.get("redirects", False),
            timeout=options.get("timeout", None),
        )

    @classmethod
    def _prepare_options(cls, endpoint: Endpoint, method: Method, **kwargs) -> dict:
        options = {
            "endpoint": endpoint,
            "method": method,
        }
        options.update(kwargs)

        options["url"] = cls._prepare_url(**options)

        return options

    @classmethod
    async def _make_request(cls, client: BaseRESTClient, **options):
        request = cls._build_request(**options)
        return await client.request(request=request, **options)

    @classmethod
    def _get_serializer(cls, **options) -> type[BaseSerializer]:
        if cls.serializer is None:
            raise TypeError("Serializer not specified")

        if not inspect.isclass(cls.serializer) or not issubclass(
            cls.serializer, BaseSerializer
        ):
            raise TypeError("The serializer must be a subclass of BaseSerializer")

        return cls.serializer

    @classmethod
    def _serialize(cls, obj: BaseModel, **options) -> dict:
        serializer = cls._get_serializer(**options)
        return serializer.serialize(obj, **options)

    @classmethod
    def _deserialize(cls, data: list | dict, many: bool = False, **options):
        serializer = cls._get_serializer(**options)
        if many:
            return serializer.deserialize_many(data=data, **options)
        return serializer.deserialize(data=data, **options)

    @classmethod
    async def create(
        cls, client: BaseRESTClient, obj: BaseModel, **kwargs
    ) -> BaseModel:

        set_pk = kwargs.pop("set_pk", True)

        options = cls._prepare_options(
            endpoint=Endpoint.CREATE, method=Method.POST, **kwargs
        )

        options["json"] = cls._serialize(obj, **options)

        response = await cls._make_request(client=client, **options)

        if set_pk:
            cls._set_pk(obj, pk=cls._get_pk(response.data))

        return obj

    @classmethod
    async def read(cls, client: BaseRESTClient, **kwargs) -> Iterable[BaseModel]:
        options = cls._prepare_options(
            endpoint=Endpoint.READ, method=Method.GET, **kwargs
        )

        response = await cls._make_request(client=client, **options)

        return cls._deserialize(data=response.data, many=True, **options)

    @classmethod
    async def read_one(cls, client: BaseRESTClient, pk: any, **kwargs) -> BaseModel:
        options = cls._prepare_options(
            endpoint=Endpoint.READ_ONE, method=Method.GET, pk=pk, **kwargs
        )

        response = await cls._make_request(client=client, **options)

        return cls._deserialize(data=response.data, many=False, **options)

    @classmethod
    async def update(cls, client: BaseRESTClient, obj: BaseModel, **kwargs) -> None:
        options = cls._prepare_options(
            endpoint=Endpoint.UPDATE, method=Method.PATCH, pk=cls._get_pk(obj), **kwargs
        )

        options["json"] = cls._serialize(obj=obj, **options)

        await cls._make_request(client=client, **options)

    @classmethod
    async def delete(cls, client: BaseRESTClient, pk: any, **kwargs) -> None:
        options = cls._prepare_options(
            endpoint=Endpoint.DELETE, method=Method.DELETE, pk=pk, **kwargs
        )

        await cls._make_request(client=client, **options)
