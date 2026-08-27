from rest_framework.routers import DefaultRouter

from .views import InventoryCategoryViewSet

# initiate default router
router = DefaultRouter()

# extend and add new router paths
# router.register(r"inventory-category", InventoryCategoryModelViewSet)
router.register(
    r"inventory-category", InventoryCategoryViewSet, basename="inventory-category"
)

urlpatterns = router.urls
