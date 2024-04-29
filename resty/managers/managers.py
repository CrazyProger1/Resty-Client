import inspect
from typing import Mapping, Iterable, Callable

from resty.clients import BaseRESTClient
from resty.enums import Endpoint, Method, Field
from resty.types import Schema, Response, Request
from resty.serializers import Serializer, BaseSerializer
from resty.managers.types import BaseManager, ResponseType
from resty.managers.builders import URLBuilder


class Manager(BaseManager):
    serializer_class = Serializer
    url_builder_class = URLBuilder

    @classmethod
    def get_serializer(cls, **kwargs) -> type[BaseSerializer]:
        serializer = kwargs.pop("serializer", cls.serializer_class)

        if not serializer:
            raise RuntimeError("Serializer not specified")

        if not (
            isinstance(serializer, BaseSerializer)
            or inspect.isclass(serializer)
            and issubclass(serializer, BaseSerializer)
        ):
            raise RuntimeError("The serializer must be a subclass of BaseSerializer")

        return serializer

    @classmethod
    def get_method(cls, endpoint: Endpoint, **kwargs) -> Method:
        method = cls.methods.get(endpoint)
        if not method:
            raise RuntimeError(f"Method not specified for endpoint: {endpoint}")

        return method

    @classmethod
    def get_field(cls, field: Field) -> str:
        field = cls.fields.get(field)

        if not field:
            raise RuntimeError(f"Field not specified: {field}")

        return field

    @classmethod
    def get_pk(cls, obj: Schema | Mapping) -> any:
        field = cls.get_field(Field.PRIMARY)

        if isinstance(obj, Mapping):
            return obj.get(field)

        return getattr(obj, field, None)

    @classmethod
    def _get_pk(cls, obj_or_pk: any) -> any:
        if isinstance(obj_or_pk, Mapping | Schema):
            return cls.get_pk(obj=obj_or_pk)
        return obj_or_pk

    @classmethod
    def _deserialize(cls, schema: type[Schema], data: any, **kwargs):
        serializer = cls.get_serializer(**kwargs)
        if isinstance(data, Mapping):
            return serializer.deserialize(schema=schema, data=data, **kwargs)
        return serializer.deserialize_many(schema=schema, data=data, **kwargs)

    @classmethod
    def _serialize(cls, obj: Schema, **kwargs):
        serializer = cls.get_serializer(**kwargs)
        return serializer.serialize(obj=obj, **kwargs)

    @classmethod
    async def _make_request(cls, client: BaseRESTClient, request: Request) -> Response:
        return await client.request(request=request)

    @classmethod
    def _prepare_url(cls, endpoint: Endpoint, **kwargs) -> str:
        url = kwargs.pop("url", None)
        base_url = kwargs.pop("base_url", None)

        if isinstance(url, str):
            return url

        return cls.url_builder_class.build(
            endpoints=cls.endpoints,
            endpoint=endpoint,
            base_url=base_url or cls.url,
            **kwargs,
        )

    @classmethod
    def _prepare_json(cls, **kwargs):
        obj = kwargs.pop("obj", None)

        if isinstance(obj, dict | list | set | tuple):
            return obj
        elif isinstance(obj, Schema):
            return cls._serialize(obj, **kwargs)
        return {}

    @classmethod
    def _prepare_request(cls, endpoint: Endpoint, **kwargs) -> Request:
        return Request(
            url=cls._prepare_url(endpoint=endpoint, **kwargs),
            method=cls.get_method(endpoint, **kwargs),
            endpoint=endpoint,
            data=kwargs.pop("data", {}),
            json=cls._prepare_json(**kwargs),
            timeout=kwargs.pop("timeout", None),
            params=kwargs.pop("params", {}),
            headers=kwargs.pop("headers", {}),
            cookies=kwargs.pop("cookies", {}),
            redirects=kwargs.pop("redirects", False),
            middleware_options=kwargs.copy(),
        )

    @classmethod
    def _handle_response(
        cls, response: Response, response_type: ResponseType, **kwargs
    ) -> any:
        if not response:
            return

        if inspect.isclass(response_type):
            if issubclass(response_type, dict | list | tuple | set):
                return response_type(response.json)
            elif issubclass(response_type, Schema):
                return cls._deserialize(
                    schema=response_type, data=response.json, **kwargs
                )

        if callable(response_type):
            try:
                return response_type(response)
            except TypeError:
                pass

        return response.json

    @classmethod
    async def create[
        T: Schema
    ](
        cls,
        client: BaseRESTClient,
        obj: Schema | Mapping,
        response_type: ResponseType = None,
        **kwargs,
    ) -> (T | None):
        request = cls._prepare_request(endpoint=Endpoint.CREATE, obj=obj, **kwargs)
        response = await cls._make_request(client=client, request=request)
        return cls._handle_response(
            response=response, response_type=response_type, **kwargs
        )

    @classmethod
    async def read[
        T: Schema
    ](
        cls, client: BaseRESTClient, response_type: ResponseType = None, **kwargs
    ) -> Iterable[T]:
        request = cls._prepare_request(endpoint=Endpoint.READ, **kwargs)
        response = await cls._make_request(client=client, request=request)
        return cls._handle_response(
            response=response, response_type=response_type, **kwargs
        )

    @classmethod
    async def read_one[
        T: Schema
    ](
        cls,
        client: BaseRESTClient,
        obj_or_pk: Schema | Mapping | any,
        response_type: ResponseType = None,
        **kwargs,
    ) -> T:

        request = cls._prepare_request(
            endpoint=Endpoint.READ_ONE, pk=cls._get_pk(obj_or_pk=obj_or_pk), **kwargs
        )
        response = await cls._make_request(client=client, request=request)
        return cls._handle_response(
            response=response, response_type=response_type, **kwargs
        )

    @classmethod
    async def update[
        T: Schema
    ](
        cls,
        client: BaseRESTClient,
        obj: Schema | Mapping,
        response_type: ResponseType = None,
        **kwargs,
    ) -> (T | None):
        request = cls._prepare_request(
            endpoint=Endpoint.UPDATE,
            pk=kwargs.pop("pk", cls.get_pk(obj)),
            obj=obj,
            **kwargs,
        )
        response = await cls._make_request(client=client, request=request)
        return cls._handle_response(
            response=response, response_type=response_type, **kwargs
        )

    @classmethod
    async def delete[
        T: Schema
    ](
        cls,
        client: BaseRESTClient,
        obj_or_pk: Schema | Mapping | any,
        response_type: ResponseType = None,
        **kwargs,
    ) -> (T | None):
        request = cls._prepare_request(
            endpoint=Endpoint.DELETE, pk=cls._get_pk(obj_or_pk=obj_or_pk), **kwargs
        )
        response = await cls._make_request(client=client, request=request)
        return cls._handle_response(
            response=response, response_type=response_type, **kwargs
        )
