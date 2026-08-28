from inventory.models import Category, Product
from rest_framework import serializers


class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "parent", "name", "slug", "is_active", "level"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "parent", "name", "slug", "is_active", "level"]


class ProductSerializerIn(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", 'name', 'slug', 'description', 'price', 'is_digital', 'is_active']

class ProductSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug']