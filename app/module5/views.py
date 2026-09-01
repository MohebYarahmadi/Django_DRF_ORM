# region IMPORTS
from inventory.models import Category, Product, Order, Product, User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .serializers import (
    CategorySerializer, ProductSerializerIn, ProductSerializerOut,
    ProductStockSerializer, OrderSerializer, UserSerializer,
    CategoryBulkSerializer,
)
# endregion IMPORTS


# region CATEGORY


class CategoryViewSet(ViewSet):
    # @extend_schema(
    #     tags=["Module 5 - Category"],
    # )
    # def list(self, request):
    #     queryset = Category.objects.all()
    #     serializer = CategorySerializer(queryset, many=True)
    #     return Response(serializer.data)

    @extend_schema(
        tags=["Module 5 - Category"],
    )
    def list(self, request):
        queryset = Category.objects.values('name', 'slug')
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=CategorySerializer,  # This links the serializer for the request body
        responses={
            201: CategorySerializer,
        },  # Expected response will be the created category
        tags=["Module 5 - Category"],
    )
    def create(self, request):  # override the create action
        # define serializer
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CategorySerializer,  # This links the serializer for the request body
        responses={
            200: CategorySerializer
        },  # Expected response will be the created category
        tags=["Module 5 - Category"],
    )
    def update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)  # fetch the existing record
        except Category.DoesNotExist:
            return Response(
                {'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(
            category, data=request.data)    # Validate data

        if serializer.is_valid():
            serializer.save()   # Update the record
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CategorySerializer,  # This links the serializer for the request body
        responses={
            200: CategorySerializer
        },  # Expected response will be the created category
        tags=["Module 5 - Category"],
    )
    def partial_update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)  # fetch the existing record
        except Category.DoesNotExist:
            return Response(
                {'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(
            category, data=request.data, partial=True)    # Validate data

        if serializer.is_valid():
            serializer.save()   # Update the record
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=["Module 5 - Category"])
    def destroy(self, request, pk=None):
        """
        Deletes a category.
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()   # Deletes Order and related OrderProducts due to
            return Response(
                {'message': 'Category deleted successfully.'},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Category.DoesNotExist:
            return Response(
                {'error': 'Category not found!'},
                status=status.HTTP_404_NOT_FOUND,
            )


class CategoryBulkViewSet(ViewSet):
    @extend_schema(
        request=CategorySerializer(many=True),
        responses={
            201: CategorySerializer(many=True)
        },  # Returns multiple inserted bojects
        tags=['Module 5 - Category'],
    )
    def create(self, request):
        # Ensure request contains a list of items
        if not isinstance(request.data, list):
            return Response(
                {'error': 'Expected a list of objects'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deserialize data (many=True allows multiple objects)
        serializer = CategorySerializer(data=request.data, many=True)

        if serializer.is_valid():
            # Convert validated data to model instances without saving yet
            categories = [Category(**item)
                          for item in serializer.validated_data]

            # Use bulk_create() to insert all at once
            created_categories = Category.objects.bulk_create(categories)

            # Serialize the created objects and return response
            return Response(
                CategorySerializer(created_categories, many=True).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=CategoryBulkSerializer, tags=['Module 5 - Category'])
    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        """
        Deletes multiple categories based on provided list of category IDs.
        Request body should contain a list of category IDs.
        """

        # Extract the list of category IDs from the request body
        serializer = CategoryBulkSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            category_ids = serializer.validated_data['ids']

            if not category_ids:
                return Response(
                    {'error': 'No category IDs provided'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Perform the deletiong of the category
            deleted_cout, _ = Category.objects.filter(
                id__in=category_ids).delete()

            # Return a response indicating how many categories were deleted
            return Response(
                {'message': f'{deleted_cout} categories deleted,'},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            # Return validation error if serializer is not valid
            return Response(
                {'error': 'Invalid data', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


# endregion CATEGORY


# region PRODUCT


class ProductViewSet(ViewSet):
    @extend_schema(
        request=ProductSerializerOut,
        responses={200: ProductSerializerOut},
        tags=["Module 5 - Product"],
    )
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializerOut(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ProductSerializerIn,
        responses={
            201: ProductSerializerOut
        },
        tags=["Module 5 - Product"],
    )
    def create(self, request):
        serializer = ProductSerializerIn(data=request.data)

        if serializer.is_valid():
            product_instance = serializer.save()
            return_serializer = ProductSerializerOut(product_instance)

            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=ProductSerializerIn,
        responses={
            200: ProductSerializerIn
        },
        tags=['Module 5 - Product'],
    )
    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializerIn(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=ProductSerializerIn,
        responses={
            200: ProductSerializerIn
        },
        tags=['Module 5 - Product'],
    )
    def partial_update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializerIn(
            product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductBulkViewSet(ViewSet):
    @extend_schema(
        request=ProductSerializerIn(many=True),
        responses={
            201: ProductSerializerIn(many=True)
        },
        tags=['Module 5 - Product'],
    )
    def create(self, request):
        if not isinstance(request.data, list):
            return Response(
                {'error': 'Expected a list of objects'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductSerializerIn(data=request.data, many=True)

        if serializer.is_valid():
            products = [Product(**item) for item in serializer.validated_data]
            created_products = Product.objects.bulk_create(products)
            return Response(
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# endregion PRODUCT


# region PRODUCT_STOCK


class ProductStockViewSet(ViewSet):
    @extend_schema(
        request=ProductStockSerializer,
        responses={201: ProductStockSerializer},
        tags=['Module 5 - ProductStock 1:1'],
    )
    def create(self, request):
        # create a product

        serializer = ProductStockSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# endregion PRODUCT_STOCK


# region ORDER
class OrderViewSet(ViewSet):
    @extend_schema(
        request=OrderSerializer,
        responses={200: OrderSerializer},
        tags=['Module 5 - Order'],
    )
    def list(self, request):
        queryset = Order.objects.all()
        serialize = OrderSerializer(queryset, many=True)
        return Response(serialize.data)

    @extend_schema(
        request=OrderSerializer,
        responses={201: OrderSerializer},
        tags=['Module 5 - Order'],
    )
    def create(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=OrderSerializer,
        responses={200: OrderSerializer},
        tags=['Module 5 - Order'],
    )
    def update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=OrderSerializer,
        responses={200: OrderSerializer},
        tags=['Module 5 - Order'],
    )
    def partial_update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# endregion ORDER


# region USER
class CreateUserViewSet(ViewSet):
    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        tags=['Moduler 4 - User'],
    )
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=UserSerializer,
        tags=['Moduler 4 - User'],
    )
    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# endregion
