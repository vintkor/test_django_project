from django.db import models
from catalog.models import CatalogProduct
from testsite.baseModel import BaseModel
from decimal import Decimal


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

    def delete(self, *args, **kwargs):
        """ При удалении корзины очищаем все Item у которых корзына была удалена """
        items = Item.objects.filter(cart_id=None)
        items.delete()
        super(Cart, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Корзины"
        verbose_name = "Корзина"

    get_total_price.short_description = "Сумма"
    get_count_items.short_description = "Кол-во товаров"


class Item(BaseModel):
    product = models.ForeignKey(CatalogProduct, verbose_name="Товар", null=True, default=None, blank=True)
    count = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="Количество")
    cart = models.ForeignKey(Cart, verbose_name="Корзина", null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return "{}".format(self.product)

    def get_total_row(self):
        return round(self.count * self.product.get_price_in_main_currency(), 2)

    @staticmethod
    def is_product_in_cart(product, cart):
        """  Проверяет есть ли товар в корзине @:return Boolean """
        try:
            Item.objects.get(product_id=product.id, cart__session=cart.session)
            return True
        except Item.DoesNotExist:
            return False

    @staticmethod
    def add_to_cart(product_id, session, count):
        """ Добавляет товар в корзину """
        cart = Cart.objects.get(session=session)
        product = CatalogProduct.objects.get(id=product_id)
        if Item.is_product_in_cart(product, cart):
            Item.update_count(product, cart, count)
        else:
            item = Item(count=count, product=product, cart=cart)
            item.save()

    @staticmethod
    def update_count(product, cart, count, update=False):
        """  Обновляет количество товара в корзине """
        if update:
            update_product = Item.objects.get(id=product.id, cart__session=cart.session)
            update_product.count = count
        else:
            update_product = Item.objects.get(product_id=product.id, cart__session=cart.session)
            old_count = update_product.count
            update_product.count = old_count + Decimal(count)
        update_product.save()

    class Meta:
        verbose_name_plural = "Товары"
        verbose_name = "Товар"

