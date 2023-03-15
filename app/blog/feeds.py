from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Article
from django.utils.translation import gettext_lazy as _


class LatestArticleFeed(Feed):
    title = _('My blog')
    link = '/blog/'
    description = _('New posts of my blog.')

    def items(self):
        return Article.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
