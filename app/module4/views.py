from inventory.models import Category, Product
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema

from .serializers import (
    CategorySerializer, ProductSerializerIn, ProductSerializerOut
)

#region CATEGORY
# ========================================
# Inserting Data with create() and save()
# ========================================
class CategoryViewSet(ViewSet):
    @extend_schema(
            request=CategorySerializer,
            responses={200: CategorySerializer},
            tags=["Module 4 - Category"],
    )
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


    @extend_schema(
            request=CategorySerializer, # This links the serializer for the request body
            responses={
                201: CategorySerializer,
            },  # Expected response will be the created category
            tags=["Module 4 - Category"],
    )
    # override the create action
    def create(self, request):
        # define serializer
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        request=CategorySerializer, # This links the serializer for the request body
        responses={
            200: CategorySerializer
        },  # Expected response will be the created category
        tags=["Module 4 - Category"],
    )
    def update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)  # fetch the existing record
        except Category.DoesNotExist:
            return Response(
                {'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data)    # Validate data

        if serializer.is_valid():
            serializer.save()   # Update the record
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class CategoryBulkViewSet(ViewSet):
    @extend_schema(
        request=CategorySerializer(many=True),
        responses={
            201: CategorySerializer(many=True)
        }, # Returns multiple inserted bojects
        tags=['Module 4 - Category'],
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
            categories = [Category(**item) for item in serializer.validated_data]

            # Use bulk_create() to insert all at once
            created_categories = Category.objects.bulk_create(categories)

            # Serialize the created objects and return response
            return Response(
                CategorySerializer(created_categories, many=True).data,
                status = status.HTTP_201_CREATED,
            )
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#endregion CATEGORY

#region PRODUCT
# ========================================
# Inserting Data with create() and save()
# ========================================
class ProductViewSet(ViewSet):
    @extend_schema(
            request=ProductSerializerOut,
            responses={200: ProductSerializerOut},
            tags=["Module 4 - Product"],
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
        tags=["Module 4 - Product"],
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
        tags=['Module 4 - Product'],
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

class ProductBulkViewSet(ViewSet):
    @extend_schema(
        request=ProductSerializerIn(many=True),
        responses={
            201: ProductSerializerIn(many=True)
        },
        tags=['Module 4 - Product'],
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
                status = status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#endregion PRODUCT