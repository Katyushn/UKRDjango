from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *


urlpatterns = [
    path('', cart_detail, name='detail'),
    path('add/<int:product_id>/', cart_add, name='add'),
    path('remove/<int:product_id>/', cart_remove, name='remove'),
    
    path('wishes/', wishes_detail, name='wishes'),
    path('wishes-add/<int:product_id>/', wishes_add, name='wishes_add'),
    path('wishes-remove/<int:product_id>/', wishes_remove, name='wishes_remove'),
]

app_name = 'cart'
