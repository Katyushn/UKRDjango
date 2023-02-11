from django.urls import path
from .views import *


urlpatterns = [
    path('apply/', coupon_apply, name='apply'),
]


app_name = 'coupons'
