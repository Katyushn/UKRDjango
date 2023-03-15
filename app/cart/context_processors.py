from .cart import Cart
from .wishes import Wishes


def cart(request):
    return {'cart': Cart(request)}


def wishes(request):
    return {'wishes': Wishes(request)}
