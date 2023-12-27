from decimal import Decimal
from typing import Any

from coupons.models import Coupon
from django.conf import settings
from shop.models import Product


class Cart:

    def __init__(self, request):
        """
        Инициализировать коризину.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def save(self):
        """Пометить сеанс как измененный."""
        self.session.modified = True

    def clear(self):
        """Очистить сеанс."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def add(self, product: Product, quantity: int = 1, override_quantity: bool = False):
        """
        Добавить товар в корзину либо обновить его количество.
        :param product: экземпляр Product для его добавления или обновления в корзине.
        :param quantity: количество товара.
        :param override_quantity: заменить колиество переданным количеством(True)
        или прибавить к существующему(False).
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product: Product):
        """
        Удалить товар из корзины.
        :param product: экземпляр Product для его удаления из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """Подсчитать общую стоимость товаров."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле
        и получить товары из базы данных.
        """
        product_ids: dict[Any, Any] | Any = self.cart.keys()
        products: Product = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчитать все товарные позиции в корзине."""
        return sum(item['quantity'] for item in self.cart.values())
