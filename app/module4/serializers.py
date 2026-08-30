from inventory.models import Category, Product, StockManagement, Order, User, OrderProduct
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

    def to_representation(self, instance):
        """Customize the representation to include stock_data"""
        # Start with the default representation
        data = super().to_representation(instance)

        # Fecth the related stock_data from the StockeManagement table
        stock_instance = StockManagement.objects.filter(
            product=instance).first()

        # If stock_data exists, add it to the response
        if stock_instance:
            data['stock_data'] = StockManagementSerializer(stock_instance).data
        else:
            data['stock_data'] = None   # In case there's no related stock data

        return data


class OrderProductSerializer(serializers.ModelSerializer):
    """Handles individual product entries within an order"""
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class OrderSerializer(serializers.ModelSerializer):
    """Handles order creation with multiple products"""
    products = OrderProductSerializer(
        many=True,
        write_only=True
    )   # Accept a list of products

    class Meta:
        model = Order
        fields = ['user', 'created_at', 'updated_at', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('products')   # Extract product list
        order = Order.objects.create(**validated_data)  # Create the order

        # Create OrderProduct entries for each product in the request
        order_products = [
            OrderProduct(order=order, **product_data) for product_data in products_data
        ]
        OrderProduct.objects.bulk_create(order_products)  # Bulk insert

        return order
