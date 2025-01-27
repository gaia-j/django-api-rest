from rest_framework import serializers
from store.models.ProductModel import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'price', 'description')

    image = serializers.ImageField(required=False, allow_null=True)