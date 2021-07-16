from catalog.models.files import ProductFile
from rest_framework import serializers
from catalog.models import Product, AttributeValue, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "slug", "title", "category",
                  "code","series", "price",
                  "description")


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ("id", "product", "title", "value",)
        

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("product", "image")


class ProductFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFile
        fields = ("product", "file")
