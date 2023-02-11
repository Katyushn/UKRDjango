from django.urls import path
from .views import *


urlpatterns = [
    path('', account, name='profile'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('password-change/', password_change, name='password_change'),

    path('edit/', edit, name='profile_edit'),

    path('subscribe/', subscribe, name='subscribe'),
    path('message/', message, name='message'),
    path('lang/', lang, name='lang'),
]

app_name = 'account'
