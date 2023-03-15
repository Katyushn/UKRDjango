from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *


urlpatterns = [
    path('create/', order_create, name='create'),
]

app_name = 'orders'
