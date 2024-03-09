from rest_framework.viewsets import ModelViewSet

from .models import Shop, Product, Basket, TotalOrderItem, Contact, Category
from .serializers import ShopSerializer, ProductSerializer, BasketSerializer, \
    TotalOrderItemSerializer, ContactSerializer, CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class BasketViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

class TotalOrderItemViewSet(ModelViewSet):
    queryset = TotalOrderItem.objects.all()
    serializer_class = TotalOrderItemSerializer





