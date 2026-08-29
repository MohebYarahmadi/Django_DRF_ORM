from inventory.models import Category, Product, StockManagement
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
        fields = ["id", 'name', 'slug', 'description',
                  'price', 'is_digital', 'is_active', 'category']


class ProductSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category']


class StockManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockManagement
        fields = ['quantity']


class ProductStockSerializer(serializers.ModelSerializer):
    stock_data = StockManagementSerializer(
        write_only=True,
        required=True
    )   # nested serailizer source

    class Meta:
        model = Product
        fields = [
            "id",
            'name',
            'slug',
            'description',
            'price',
            'is_digital',
            'is_active',
            'category',
            'stock_data',   # nested data
        ]

    def create(self, validated_data):
        # Extract data from validated data (actually remove it and store it in new var)
        stock_data = validated_data.pop('stock_data', None)
        # stock_data not existed here anymore in validated_data. we can save product data
        product = Product.objects.create(**validated_data)
        # create stockmanagement data with stock_data var and pass in product too to get pk for
        StockManagement.objects.create(product=product, **stock_data)

        return product
