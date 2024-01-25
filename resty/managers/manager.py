from typing import Iterable

from pydantic import BaseModel

from resty.types import (
    BaseManager,
    BaseRESTClient
)
from resty.types import (
    Request,
    Response
)
from resty.enums import (
    Endpoint
)


class Manager(BaseManager):
    @classmethod
    def _get_endpoint(cls, endpoint: Endpoint, primary_key: any = None) -> str:
        return cls.endpoints.get(
            endpoint,
            cls.endpoints.get(
                endpoint.BASE,
                ''
            ))

    @classmethod
    async def create(cls, client: BaseRESTClient, obj: BaseModel, **kwargs) -> BaseModel:
        pass

    @classmethod
    async def read(cls, client: BaseRESTClient, **kwargs) -> Iterable[BaseModel]:
        request = Request(
            method='GET',
            url=cls._get_endpoint(Endpoint.READ),
        )
        response = await client.request(
            request=request,
            **kwargs
        )

    @classmethod
    async def read_one(cls, client: BaseRESTClient, pk: any, **kwargs) -> BaseModel:
        pass

    @classmethod
    async def update(cls, client: BaseRESTClient, obj: BaseModel, **kwargs) -> None:
        pass

    @classmethod
    async def delete(cls, client: BaseRESTClient, pk: any, **kwargs) -> None:
        pass
