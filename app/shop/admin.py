from .models import Product, Filter, FilterName
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from django.db import models
from django.forms import CheckboxSelectMultiple


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'show_img', 'price', 'stock', 'category', 'created', 'updated', 'status', 'publish', 'is_published',)
#     list_display_links = ('title',)
#     search_fields = ('title',)
#     list_editable = ('price', 'stock', 'is_published',)
#     list_filter = ('status', 'category', 'is_published',)
#     prepopulated_fields = {'slug': ('title',)}
#     date_hierarchy = 'publish'
#     ordering = ['-id', 'publish']
#     save_on_top = True
#
#
# @admin.register(FilterName)
# class FilterNameAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title',)
#     list_display_links = ('title',)
#
#
# @admin.register(Filter)
# class FilterAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'parent')
#     list_display_links = ('title',)
#     ordering = ['parent', 'title']
