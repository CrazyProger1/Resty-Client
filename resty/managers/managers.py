from typing import Mapping, Iterable

from resty.managers.types import BaseManager
from resty.types import Schema


class Manager(BaseManager):
    @classmethod
    async def create[
        T: Schema
    ](cls, obj: Schema | Mapping, response_schema: type[T] = None, **kwargs) -> (
        T | None
    ):
        pass

    @classmethod
    async def read[T: Schema](cls, response_schema: type[T], **kwargs) -> Iterable[T]:
        pass

    @classmethod
    async def read_one[
        T: Schema
    ](cls, obj_or_pk: Schema | Mapping | any, response_schema: type[T], **kwargs) -> T:
        pass

    @classmethod
    async def update[
        T: Schema
    ](cls, obj: Schema | Mapping, response_schema: type[T] = None, **kwargs) -> (
        T | None
    ):
        pass

    @classmethod
    async def delete[
        T: Schema
    ](
        cls,
        obj_or_pk: Schema | Mapping | any,
        response_schema: type[T] = None,
        **kwargs,
    ) -> (T | None):
        pass
