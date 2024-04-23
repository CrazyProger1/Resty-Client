from resty.serializers import Serializer
from resty.enums import Endpoint

from schemas import (
    ProductCreateSchema,
    ProductReadSchema,
    ProductUpdateSchema
)


class ProductSerializer(Serializer):
    schemas = {
        Endpoint.CREATE: ProductCreateSchema,
        Endpoint.READ: ProductReadSchema,
        Endpoint.READ_ONE: ProductReadSchema,
        Endpoint.UPDATE: ProductUpdateSchema
    }
