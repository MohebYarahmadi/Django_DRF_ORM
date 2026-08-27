from inventory.models import Category
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import InventoryCategorySerializer

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
