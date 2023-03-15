from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from ckeditor_uploader.fields import RichTextUploadingField
from slugify import slugify
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    STATUS_CHOICES = (
        ('standard', _('standard')),
        ('top', _('Top')),
    )
    CURRENCY_CHOICES = (
        ('UAH', 'UAH'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(max_length=250, unique=True, null=False, blank=False, verbose_name=_('Link'))
    description = models.CharField(max_length=250, verbose_name=_('Description'))
    author = models.ForeignKey(User, editable=False, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_('Author'))
    code = models.CharField(max_length=250, verbose_name=_('Code'))
    available = models.BooleanField(default=True, verbose_name=_('Available'))
    intro = models.TextField(null=True, blank=True, verbose_name=_('Intro'))
    param_name_1 = models.SlugField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Param name №1'))
    param_name_2 = models.SlugField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Param name №2'))
    param_name_3 = models.SlugField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Param name №3'))
    param_name_4 = models.SlugField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Param name №4'))
    param_name_5 = models.SlugField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Param name №5'))
    param_text_1 = models.TextField(null=True, blank=True, verbose_name=_('Param text №1'))
    param_text_2 = models.TextField(null=True, blank=True, verbose_name=_('Param text №2'))
    param_text_3 = models.TextField(null=True, blank=True, verbose_name=_('Param text №3'))
    param_text_4 = models.TextField(null=True, blank=True, verbose_name=_('Param text №4'))
    param_text_5 = models.TextField(null=True, blank=True, verbose_name=_('Param text №5'))
    img1 = models.ImageField(upload_to='product/%Y/%m/', blank=True, verbose_name=_('Image'))
    img2 = models.ImageField(upload_to='product/%Y/%m/', blank=True, verbose_name=_('Image'))
    img3 = models.ImageField(upload_to='product/%Y/%m/', blank=True, verbose_name=_('Image'))
    img4 = models.ImageField(upload_to='product/%Y/%m/', blank=True, verbose_name=_('Image'))
    img5 = models.ImageField(upload_to='product/%Y/%m/', blank=True, verbose_name=_('Image'))
    video1 = models.CharField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Video'))
    video2 = models.CharField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Video'))
    video3 = models.CharField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Video'))
    video4 = models.CharField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Video'))
    video5 = models.CharField(max_length=250, unique=True, null=True, blank=True, verbose_name=_('Video'))
    text1 = RichTextUploadingField(null=True, blank=True, verbose_name=_('Text'))
    text2 = RichTextUploadingField(null=True, blank=True, verbose_name=_('Text'))
    text3 = RichTextUploadingField(null=True, blank=True, verbose_name=_('Text'))
    text4 = RichTextUploadingField(null=True, blank=True, verbose_name=_('Text'))
    text5 = RichTextUploadingField(null=True, blank=True, verbose_name=_('Text'))
    category = models.ForeignKey('builder.Category', null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('Category'))
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default='standard', verbose_name=_('Status'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    stock = models.PositiveIntegerField(verbose_name=_('Stock'))
    currency = models.CharField(max_length=250, choices=CURRENCY_CHOICES, default='UAH', verbose_name=_('Currency'))
    quantity = models.IntegerField(null=True, blank=True, verbose_name=_('Quantity'))
    filter = models.ManyToManyField('shop.Filter', blank=True, verbose_name=_('Filter'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    publish = models.DateTimeField(default=timezone.now, verbose_name=_('Publish'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    def get_absolute_url(self):
        return reverse('builder:article_product', kwargs={"item_slug": self.category.slug, "item_id": self.category.pk, "value_slug": self.slug, "value_id": self.pk})

    # def save(self, *args, **kwargs):
    #     super(Products, self).save()
    #     if not self.slug.endswith('-' + str(self.id)):
    #         self.slug += '-' + str(self.id)
    #         super(Products, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created']


class Term(models.Model):
    delivery = RichTextUploadingField(null=True, blank=True, verbose_name=_('Delivery'))
    payment = RichTextUploadingField(null=True, blank=True, verbose_name=_('Payment'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return _("Условия доставки и оплаты")

    class Meta:
        verbose_name = _('Условия')
        verbose_name_plural = _('Условия')
        ordering = ['pk']


class FilterName(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Filter name')
        verbose_name_plural = _('Filter name')
        ordering = ['title']


class Filter(models.Model):
    parent = models.ForeignKey('shop.FilterName', null=True, blank=True, on_delete=models.PROTECT, verbose_name=_('Parent'))
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return self.parent.title + ' -> ' + self.title

    class Meta:
        verbose_name = _('Filter')
        verbose_name_plural = _('Filters')
        ordering = ['parent']
