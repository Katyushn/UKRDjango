from django.urls import path
from django.urls import path, include
from django.http import HttpResponse, HttpResponseNotFound
from .views import *
from blog.feeds import LatestArticleFeed
from blog.views import article_share_email, BlogSearch, BlogTag


urlpatterns = [
    path('', home, name='home'),
    path('blog/feed/', LatestArticleFeed(), name='blog_feed'),
    path('blog/search/', BlogSearch.as_view(), name='blog_search'),
    path('blog/tag/<slug:item_slug>-<int:item_id>/', BlogTag.as_view(), name='blog_tag'),
    path('<slug:item_slug>-<int:item_id>/', switcher_page_blog_shop, name='page_blog_shop'),
    path('<slug:item_slug>-<int:item_id>/<slug:value_slug>-<int:value_id>/', switcher_article_product, name='article_product'),
    path('<slug:item_slug>-<int:item_id>/<slug:value_slug>-<int:value_id>/share/', article_share_email, name='article_share'),
    path('<slug:item_slug>/', switcher_menu, name='menu'),
]

app_name = 'builder'
