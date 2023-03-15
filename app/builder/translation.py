from modeltranslation.translator import register, TranslationOptions
from .models import Category, Menu, Text, Html, Tag

# python manage.py update_translation_fields


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'intro')


@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Text)
class TextTranslationOptions(TranslationOptions):
    fields = ('text',)


@register(Html)
class HtmlTranslationOptions(TranslationOptions):
    fields = ('html',)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('title',)
