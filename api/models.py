from django.db import models
from django.db.models import F, Sum
from new_user.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='contacts', null=True,
                             blank=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = "Контактные данные"

    def __str__(self):
        return f'{self.city}, ул.{self.street}, дом {self.house} ({self.phone})'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Продукт')
    description = models.CharField(max_length=100, verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} {self.price}"

class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория магазина'
        verbose_name_plural = "Категории магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Менеджер', null=True, blank=True)
    url = models.URLField(verbose_name='Ссылка на сайт', null=True, blank=True)
    name = models.CharField(max_length=40, verbose_name='Магазин', unique=True)
    state = models.BooleanField(default=True, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата открытия")
    product = models.ManyToManyField(Product, through="ProductPosition", related_name="shops")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Магазины"
        ordering = ('-name',)

    def __str__(self):
        return f"{self.name} {self.state} {self.category}"


class ProductPosition(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='positions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='positions')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    external_id = models.PositiveIntegerField(verbose_name='Внешний ИД')
################################################################################################


class Basket(models.Model):
    shop = models.ManyToManyField(Shop, through="BasketItem", related_name='basket_shop')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name_plural = 'Позиции корзины'

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='baskets', verbose_name='Заказ №')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='baskets', blank=False, null=True)
    product = models.ForeignKey(ProductPosition, on_delete=models.SET_NULL, related_name='products_prices', verbose_name='Заказаные родукты', null=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количетсво")

#######################################################################################


class TotalOrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    basket = models.ManyToManyField(Basket, through="OrderPosition", verbose_name='Корзина')

    class Meta:
        verbose_name_plural = 'Итоговый заказ'


class OrderPosition(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='order_basket')
    total_order = models.ForeignKey(TotalOrderItem, on_delete=models.CASCADE, related_name='pos')

    class Meta:
        verbose_name_plural = 'Корзина товаров'

