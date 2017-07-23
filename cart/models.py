from django.db import models
from catalog.models import CatalogProduct
from testsite.baseModel import BaseModel


class Cart(BaseModel):
    session = models.CharField(max_length=255, verbose_name="Сессия")

    def __str__(self):
        return "{}".format(self.id)

    def get_count_items(self):
        return Item.objects.filter(cart=self).count()

    def get_total_price(self):
        total_price = 0
        items = Item.objects.filter(cart=self)
        for item in items:
            total_price += item.product.get_price_in_main_currency() * item.count
        return round(total_price, 2)

    class Meta:
        verbose_name_plural = "Корзины"
        verbose_name = "Корзина"

    get_total_price.short_description = "Сумма"
    get_count_items.short_description = "Кол-во товаров"


class Item(BaseModel):
    product = models.ForeignKey(CatalogProduct, verbose_name="Товар", null=True, default=None, blank=True)
    count = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Количество")
    cart = models.ForeignKey(Cart, verbose_name="Корзина", null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return "{}".format(self.product)

    class Meta:
        verbose_name_plural = "Товары"
        verbose_name = "Товар"

