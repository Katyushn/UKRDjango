from django.contrib import admin
from .models import Profile, Message, Subscribe


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'message']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['email', ]