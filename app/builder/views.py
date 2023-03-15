from django.shortcuts import render, get_object_or_404
from blog.views import BlogCategory, BlogArticle
from shop.views import ShopCategory
from .models import Category, Menu, Template
from blog.models import Article
from shop.models import Product
from .context import get_context


def switcher_page_blog_shop(request, item_slug, item_id):
    category = get_object_or_404(Category, slug=item_slug, pk=item_id)
    if category.type == 'blog':
        return BlogCategory.as_view()(request, blog_category_slug=item_slug, blog_category_id=item_id)
    else:
        return ShopCategory.as_view()(request, shop_category_slug=item_slug, shop_category_id=item_id)


def switcher_article_product(request, item_slug, item_id, value_slug, value_id):
    category = get_object_or_404(Category, slug=item_slug, pk=item_id)
    if category.type == 'blog':
        return BlogArticle.as_view()(request, blog_category_slug=item_slug, blog_category_id=item_id, post_slug=value_slug, post_id=value_id)
    else:
        return ShopCategory.as_view()(request, shop_category_slug=item_slug, shop_category_id=item_id, product_slug=value_slug, product_id=value_id)


def switcher_menu(request, item_slug):
    menu = Menu.objects.all()
    for item in menu:
        if item.type == 'template' and item.slug == item_slug:
            template = Template.objects.get(pk=item.template.id).slug
            context = get_context()
            context['title'] = item.title
            return render(request, template, context)
        if item.type == 'category' and item.slug == item_slug:
            category = get_object_or_404(Category, pk=item.category.id)
            if category.type == 'blog':
                return BlogCategory.as_view()(request, blog_category_slug=category.slug, blog_category_id=category.pk)
            else:
                return ShopCategory.as_view()(request, shop_category_slug=category.slug, shop_category_id=category.pk)
        if item.type == 'article' and item.slug == item_slug:
            article = Article.objects.get(pk=item.post.id)
            if article.category:
                category = get_object_or_404(Category, pk=article.category.id)
                return BlogArticle.as_view()(request, blog_category_slug=category.slug, blog_category_id=category.id, post_slug=article.slug, post_id=article.id)
            else:
                return BlogArticle.as_view()(request, blog_category_slug=None, blog_category_id=None, post_slug=article.slug, post_id=article.id)
        if item.type == 'product' and item.slug == item_slug:
            product = Product.objects.get(pk=item.product.id)
            category = get_object_or_404(Category, pk=product.category.id)
            return ShopCategory.as_view()(request, shop_category_slug=category.slug, shop_category_id=category.id,product_slug=product.slug, product_id=product.id)
    return get_object_or_404(Menu, pk=100000000)


def home(request):
    item = get_object_or_404(Menu, default=True)
    if item.type == 'template':
        template = Template.objects.get(pk=item.template.id).slug
        context = get_context()
        context['title'] = item.title
        return render(request, template, context)
    if item.type == 'category':
        category = get_object_or_404(Category, pk=item.category.id)
        if category.type == 'blog':
            return BlogCategory.as_view()(request, blog_category_slug=category.slug, blog_category_id=category.pk)
        else:
            return ShopCategory.as_view()(request, shop_category_slug=category.slug, shop_category_id=category.pk)
    if item.type == 'article':
        article = Article.objects.get(pk=item.post.id)
        category = get_object_or_404(Category, pk=article.category.id)
        return BlogArticle.as_view()(request, blog_category_slug=category.slug, blog_category_id=category.id,
                                     post_slug=article.slug, post_id=article.id)
    if item.type == 'product':
        product = Product.objects.get(pk=item.product.id)
        category = get_object_or_404(Category, pk=product.category.id)
        return ShopCategory.as_view()(request, shop_category_slug=category.slug, shop_category_id=category.id,
                                      product_slug=product.slug, product_id=product.id)
