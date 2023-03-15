from modeltranslation.translator import register, TranslationOptions
from .models import Article


@register(Article)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'intro', 'body')


