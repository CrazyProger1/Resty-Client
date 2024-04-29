import inspect
from typing import Mapping, Iterable

from resty.clients import BaseRESTClient
from resty.enums import Endpoint, Method, Field
from resty.types import Schema, Response, Request
from resty.serializers import Serializer, BaseSerializer
from resty.managers.types import BaseManager, ResponseType
from resty.managers.builders import URLBuilder


class Manager(BaseManager):
    serializer_class = Serializer
    url_builder_class = URLBuilder

    def __init__(self, client: BaseRESTClient = None):
        self._client = client

    def get_serializer(self, **kwargs) -> type[BaseSerializer]:
        serializer = kwargs.pop("serializer", self.serializer_class)

        if not serializer:
            raise RuntimeError("Serializer not specified")

        if not (
                isinstance(serializer, BaseSerializer)
                or inspect.isclass(serializer)
                and issubclass(serializer, BaseSerializer)
        ):
            raise RuntimeError("The serializer must be a subclass of BaseSerializer")

        return serializer

    def get_method(self, endpoint: Endpoint, **kwargs) -> Method:
        method = self.methods.get(endpoint)
        if not method:
            raise RuntimeError(f"Method not specified for endpoint: {endpoint}")

        return method

    def get_field(self, field: Field) -> str:
        field = self.fields.get(field)

        if not field:
            raise RuntimeError(f"Field not specified: {field}")

        return field

    def get_pk(self, obj: Schema | Mapping) -> any:
        field = self.get_field(Field.PRIMARY)

        if isinstance(obj, Mapping):
            return obj.get(field)

        return getattr(obj, field, None)

    def _get_pk(self, obj_or_pk: any) -> any:
        if isinstance(obj_or_pk, Mapping | Schema):
            return self.get_pk(obj=obj_or_pk)
        return obj_or_pk

    def _deserialize(self, schema: type[Schema], data: any, **kwargs):
        serializer = self.get_serializer(**kwargs)
        if isinstance(data, Mapping):
            return serializer.deserialize(schema=schema, data=data, **kwargs)
        return serializer.deserialize_many(schema=schema, data=data, **kwargs)

    def _serialize(self, obj: Schema, **kwargs):
        serializer = self.get_serializer(**kwargs)
        return serializer.serialize(obj=obj, **kwargs)

    def _get_client(self, **kwargs) -> BaseRESTClient:
        client = kwargs.pop("client", self._client)

        if not client:
            raise TypeError(
                "REST Client not specified. Pass it to the constructor or via kwargs"
            )

        if not isinstance(client, BaseRESTClient):
            raise TypeError("Client must inherit from BaseRESTClient")

        return client

    async def _make_request(self, request: Request, **kwargs) -> Response:
        client = self._get_client(**kwargs)
        return await client.request(request=request)

    def _prepare_url(self, endpoint: Endpoint, **kwargs) -> str:
        url = kwargs.pop("url", None)
        base_url = kwargs.pop("base_url", None)

        if isinstance(url, str):
            return url

        return self.url_builder_class.build(
            endpoints=self.endpoints,
            endpoint=endpoint,
            base_url=base_url or self.url,
            **kwargs,
        )

    def _prepare_json(self, **kwargs):
        obj = kwargs.pop("obj", None)

        if isinstance(obj, dict | list | set | tuple):
            return obj
        elif isinstance(obj, Schema):
            return self._serialize(obj, **kwargs)
        return {}

    def _prepare_request(self, endpoint: Endpoint, **kwargs) -> Request:
        return Request(
            url=self._prepare_url(endpoint=endpoint, **kwargs),
            method=self.get_method(endpoint, **kwargs),
            endpoint=endpoint,
            data=kwargs.pop("data", {}),
            json=self._prepare_json(**kwargs),
            timeout=kwargs.pop("timeout", None),
            params=kwargs.pop("params", {}),
            headers=kwargs.pop("headers", {}),
            cookies=kwargs.pop("cookies", {}),
            redirects=kwargs.pop("redirects", False),
            middleware_options=kwargs.copy(),
        )

    def _handle_response(
            self, response: Response, response_type: ResponseType, **kwargs
    ) -> any:
        if not response:
            return

        if inspect.isclass(response_type):
            if issubclass(response_type, dict | list | tuple | set):
                return response_type(response.json)
            elif issubclass(response_type, Schema):
                return self._deserialize(
                    schema=response_type, data=response.json, **kwargs
                )

        if callable(response_type):
            try:
                return response_type(response)
            except TypeError:
                pass

        return response.json

    async def create[
    T: Schema
    ](
            self,
            obj: Schema | Mapping,
            response_type: ResponseType = None,
            **kwargs,
    ) -> (
            T | None
    ):
        request = self._prepare_request(endpoint=Endpoint.CREATE, obj=obj, **kwargs)
        response = await self._make_request(request=request, **kwargs)
        return self._handle_response(
            response=response, response_type=response_type, **kwargs
        )

    async def read[
    T: Schema
    ](self, response_type: ResponseType = None, **kwargs) -> Iterable[T]:
        request = self._prepare_request(endpoint=Endpoint.READ, **kwargs)
        response = await self._make_request(request=request, **kwargs)
        return self._handle_response(
            response=response, response_type=response_type, **kwargs
        )

    async def read_one[
    T: Schema
    ](
            self,
            obj_or_pk: Schema | Mapping | any,
            response_type: ResponseType = None,
            **kwargs,
    ) -> T:

        request = self._prepare_request(
            endpoint=Endpoint.READ_ONE, pk=self._get_pk(obj_or_pk=obj_or_pk), **kwargs
        )
        response = await self._make_request(request=request, **kwargs)
        return self._handle_response(
            response=response, response_type=response_type, **kwargs
        )

    async def update[
    T: Schema
    ](
            self,
            obj: Schema | Mapping,
            response_type: ResponseType = None,
            **kwargs,
    ) -> (
            T | None
    ):
        request = self._prepare_request(
            endpoint=Endpoint.UPDATE,
            pk=kwargs.pop("pk", self.get_pk(obj)),
            obj=obj,
            **kwargs,
        )
        response = await self._make_request(request=request, **kwargs)
        return self._handle_response(
            response=response, response_type=response_type, **kwargs
        )

    async def delete[
    T: Schema
    ](
            self,
            obj_or_pk: Schema | Mapping | any,
            response_type: ResponseType = None,
            **kwargs,
    ) -> (T | None):
        request = self._prepare_request(
            endpoint=Endpoint.DELETE, pk=self._get_pk(obj_or_pk=obj_or_pk), **kwargs
        )
        response = await self._make_request(request=request, **kwargs)
        return self._handle_response(
            response=response, response_type=response_type, **kwargs
        )
