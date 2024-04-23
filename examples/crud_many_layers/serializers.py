from resty.serializers import Serializer

from schemas import ProductSchema


class ProductSerializer(Serializer):
    schema = ProductSchema
