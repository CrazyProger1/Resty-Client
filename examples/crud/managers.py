from resty.enums import (
    Endpoint,
    Field
)
from resty.managers import Manager

from serializers import ProductSerializer


class ProductManager(Manager):
    serializer = ProductSerializer
    endpoints = {
        Endpoint.CREATE: '/products/',
        Endpoint.READ: '/products/',
        Endpoint.READ_ONE: '/products/{pk}/',
        Endpoint.UPDATE: '/products/{pk}/',
        Endpoint.DELETE: '/products/{pk}/',
    }
    fields = {
        Field.PRIMARY: 'id',
    }
