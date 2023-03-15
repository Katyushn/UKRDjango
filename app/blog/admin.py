from .models import Article, Comment
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms import CheckboxSelectMultiple
from django.db import models
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from mptt.admin import DraggableMPTTAdmin
from builder.models import Category, Template, Menu
from django.utils.translation import gettext_lazy as _


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'show_img', 'category', 'author', 'created',
                    'updated', 'status', 'publish', 'is_published',)
    list_display_links = ('title',)
    search_fields = ('title',)
    list_editable = ('is_published',)
    # list_filter = ('status', 'category', 'is_published',)
    list_filter = ('created',
                   # ('status', ChoiceDropdownFilter),
                   # ('category', DropdownFilter),
                   # ('is_published', RelatedDropdownFilter),
                   )
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['-id', 'publish']
    save_on_top = True

    def show_img(self, obj):
        if obj.img:
            return mark_safe(f'<img src="{obj.img.url}" width="75">')
        else:
            return '-'

    show_img.short_description = _('Images')

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(type='blog')
        if db_field.name == "template":
            kwargs["queryset"] = Template.objects.filter(type='article')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def delete_queryset(self, request, queryset):
        for item in queryset:
            menus = Menu.objects.filter(post=item.id)
            for menu in menus:
                menu.post = None
                menu.save()
            item.delete()

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

