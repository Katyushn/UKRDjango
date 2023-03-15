from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .models import Product
from builder.models import Category
from django.views.generic import ListView, DetailView
from cart.forms import CartAddProductForm, WishesAddProductForm
from django.utils.translation import gettext_lazy as _


class ShopCategory(ListView):
    paginate_by = 25
    model = Product
    template_name = 'shop/category.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('All products')
        context['category'] = Category.objects.all()
        # context['css'] = 'css/style.css'

        return context

    def get_queryset(self):
        return Product.objects.all()


class ShopCategory (ShopCategory):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['shop_category_slug'], pk=self.kwargs['shop_category_id'])
        context['title'] = context['category'].title
        return context

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['shop_category_id']).select_related('category')


class ShopProduct (DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'default/shop/product.html'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        get_object_or_404(Product.objects.filter(
            category__slug=self.kwargs['shop_category_slug'],
            category_id=self.kwargs['shop_category_id'],
            slug=self.kwargs['product_slug'],
            id=self.kwargs['product_id']))
        context['title'] = 'Product'
        context['menu'] = Category.objects.all()
        # context['css'] = 'css/style.css'
        context['cart_product_form'] = CartAddProductForm()
        context['wishes_product_form'] = WishesAddProductForm()
        return context


def error404(request, exception):
    response = render(request, '404.html')
    response.status_code = 404
    return response