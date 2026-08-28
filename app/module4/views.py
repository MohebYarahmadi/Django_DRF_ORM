from inventory.models import Category, Product
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema

from .serializers import (
    CategorySerializer, InventoryCategorySerializer,
    ProductSerializerIn, ProductSerializerOut
)

# # Use ModelViewSet
# class InventoryCategoryModelViewSet(ModelViewSet):
#     queryset = Category.objects.all()  # fetch all categories
#     serializer_class = InventoryCategorySerializer  # use the serializer


# Use ViewSet
class InventoryCategoryViewSet(ViewSet):
    def list(self, request):
        queryset = Category.objects.all()
        serializer = InventoryCategorySerializer(queryset, many=True)
        return Response(serializer.data)


class InventoryProductViewSet(ViewSet):
    def list(self, reuqest):
        queryset = Product.objects.all()
        serializer = ProductSerializerIn(queryset, many=True)
        return Response(serializer.data)


# ========================================
# Inserting Data with create() and save()
# ========================================
class CategoryViewSet(ViewSet):
    @extend_schema(
            request=CategorySerializer, # This links the serializer for the request body
            responses={
                201: CategorySerializer
            },  # Expected response will be the created category
            tags=["Module 4"],
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


# ========================================
# Inserting Data with create() and save()
# ========================================
class ProductViewSet(ViewSet):
    @extend_schema(
        request=ProductSerializerIn,
        responses={
            201: ProductSerializerOut
        },
        tags=["Module 4"],
    )

    def create(self, request):
        serializer = ProductSerializerIn(data=request.data)

        if serializer.is_valid():
            product_instance = serializer.save()
            return_serializer = ProductSerializerOut(product_instance)

            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)