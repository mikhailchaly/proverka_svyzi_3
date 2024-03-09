from django.db.models import F, Sum, Count
from django.db.models.expressions import result
from rest_framework import serializers
from .models import Shop, Product, ProductPosition, Basket, BasketItem, TotalOrderItem, Contact, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


##############################################################################################################
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", 'price']

class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPosition
        fields = ["product", "quantity", "price", 'external_id']

class ShopSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Shop
        fields = ["id", "user", "name", "category", "state", "created_at", "contact", 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        shop = super().create(validated_data)

        for position in positions:
            ProductPosition.objects.create(shop=shop, **position)
        return shop

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        shop = super().update(instance, validated_data)

        for position in positions:
            ProductPosition.objects.update_or_create(
                shop=shop,
                product=position.get('product'),
                default={
                    "quantity": position.get('quantity'),
                    'price': position.get('price')
                }
            )
        return shop

#####################################################################################

class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['product', 'quantity']



class BasketSerializer(serializers.ModelSerializer):

    total_summa = serializers.SerializerMethodField("get_total_summa", read_only=True)

    baskets = BasketItemSerializer(many=True)

    class Meta:
        model = Basket
        fields = ['user', "shop", "created_at", "baskets", "total_summa"]

    def get_total_summa(self, obj):
        x = obj.baskets.annotate(per_item_price=F('product_id__price')*F('quantity')).annotate(total_summa=Sum('per_item_price')).values('total_summa')
        return x

    # В вашем примере querydata - это json. Вы можете преобразовать json в dict следующим образом:
    # import json
    #
    # from django.core import serializers
    # querydata = serializers.serialize("json", query)
    # querydata = json.loads(querydata).  # This is Python dictionary

    def create(self, validated_data):
        baskets = validated_data.pop('baskets')
        # if self.products_prices in self.shop: # так не работает
        basket = super().create(validated_data)

        for position in baskets:
            BasketItem.objects.create(basket=basket, **position)
        return basket

    def update(self, instance, validated_data, summa=None):
        baskets = validated_data.pop('baskets')
        basket = super().update(instance, validated_data)

        for position in baskets:
            BasketItem.objects.update_or_create(
                basket=basket,
                shop=position.get("shop"),
                default={
                    'product': position.get('product'),
                    'quantity': position.get('quantity')
                }
            )

        return basket


class TotalOrderItemSerializer(serializers.ModelSerializer):
    order_item = BasketSerializer(many=True, read_only=True)

    class Meta:
        model = TotalOrderItem
        fields = ['user', 'order_item']




