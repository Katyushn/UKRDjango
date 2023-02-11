from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .wishes import Wishes
from .forms import CartAddProductForm, WishesAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                            initial={'quantity': item['quantity'],
                            'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'default/cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})


def wishes_add(request, product_id):
    wishes = Wishes(request)
    product = get_object_or_404(Product, id=product_id)
    form = WishesAddProductForm(request.POST)
    if form.is_valid():
        wishes.add(product=product)
    return redirect('cart:wishes')


def wishes_remove(request, product_id):
    wishes = Wishes(request)
    product = get_object_or_404(Product, id=product_id)
    wishes.remove(product)
    return redirect('cart:wishes')


def wishes_detail(request):
    pass
    # cart = Cart(request)
    # for item in cart:
    #     item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    # coupon_apply_form = CouponApplyForm()
    # return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})