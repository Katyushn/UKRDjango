"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import ArticleSitemap
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.views import *
from django.contrib.auth import views as auth_views

sitemaps = {
    'posts': ArticleSitemap,
}

urlpatterns = [

    path('social/', include('social_django.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('account/', include('account.urls', namespace='account')),
    path('register/reset-password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('register/reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('register/reset-password-form/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include('builder.urls', namespace='builder')),
    # prefix_default_language=False  # hide prefix whit original language
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# INSTALLED_APPS -> admin.py
admin.autodiscover()

# admin site-bar
admin.site.enable_nav_sidebar = False

handler404 = 'blog.views.error404'
