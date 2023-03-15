from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Code'))
    valid_from = models.DateTimeField(verbose_name=_('Date now'))
    valid_to = models.DateTimeField(verbose_name=_('Date end'))
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_('Discount'))
    active = models.BooleanField(verbose_name=_('Status'))

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
        ordering = ('-valid_from',)

    def __str__(self):
        return self.code
