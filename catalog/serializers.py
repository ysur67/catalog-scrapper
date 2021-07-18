from catalog.models.files import ProductFile
from rest_framework import serializers
from catalog.models import Product, AttributeValue, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    folder_category = serializers.SerializerMethodField("get_folder_category")

    def get_folder_category(self, _):
        return "Сварочное оборудование"

    class Meta:
        model = Product
        fields = ("id", "slug", "title", "folder_category", "category",
                  "code","series", "price", "image",
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
