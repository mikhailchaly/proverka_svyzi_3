
from django.contrib import admin
from django.core import servers
from django.db.models import F, Sum
from rest_framework import request, serializers


from . models import Product, Shop, ProductPosition, Basket, BasketItem, TotalOrderItem, OrderPosition
from . serializers import BasketSerializer


class ProductPositionInline(admin.TabularInline):
    model = ProductPosition
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'state', 'created_at']
    inlines = [ProductPositionInline]


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 2


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):

    total_summa = BasketSerializer.get_total_summa #Это работает, но выдает queriset


    list_display = ['user', 'created_at', 'total_summa']
    inlines = [BasketItemInline]


class OrderPositionInline(admin.TabularInline):
    model = OrderPosition
    extra = 3


@admin.register(TotalOrderItem)
class TotalOrderItemAdmin(admin.ModelAdmin):
    list_display = ['user']
    inlines = [OrderPositionInline]

