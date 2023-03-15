from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_('Firstname'))
    last_name = models.CharField(max_length=50, verbose_name=_('Lastname'))
    email = models.EmailField(verbose_name=_('Email'))
    address = models.CharField(max_length=250, verbose_name=_('Address'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    paid = models.BooleanField(default=False, verbose_name=_('Paid'))
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_('Coupon'))
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_('Discount'))

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.orderitem_set.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Order'))
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_('Product'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

