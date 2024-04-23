from resty.enums import (
    Endpoint,
    Field
)
from resty.managers import Manager

from serializers import ProductSerializer


class UserProductManager(Manager):
    serializer = ProductSerializer
    endpoints = {
        Endpoint.CREATE: 'users/{user_pk}/products/',
        Endpoint.READ: 'users/{user_pk}/products/',
        Endpoint.READ_ONE: 'users/{user_pk}/products/{pk}/',
        Endpoint.UPDATE: 'users/{user_pk}/products/{pk}/',
        Endpoint.DELETE: 'users/{user_pk}/products/{pk}/',
    }
    fields = {
        Field.PRIMARY: 'id',
    }
