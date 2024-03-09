from rest_framework.routers import DefaultRouter

from api.views import ShopViewSet, ProductViewSet, BasketViewSet, TotalOrderItemViewSet, ContactViewSet, CategoryViewSet

router = DefaultRouter()


router.register(r"shop", ShopViewSet)
router.register('product', ProductViewSet)
router.register('basket', BasketViewSet),
router.register("total", TotalOrderItemViewSet)
router.register("contact", ContactViewSet)
router.register('category', CategoryViewSet)

urlpatterns = router.urls

