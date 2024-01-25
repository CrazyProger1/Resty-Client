from resty.serializers import Serializer

from schemas import Product


class ProductSerializer(Serializer):
    schema = Product
