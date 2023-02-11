from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_('User'))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('Birthday'))
    photo = models.ImageField(upload_to='user/%Y/%m/', blank=True, verbose_name=_('Foto'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['id']

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Subscribe(models.Model):
    email = models.EmailField(null=False, blank=False, verbose_name='Email')

    class Meta:
        verbose_name = _('Subscriptions')
        verbose_name_plural = _('Subscriptions')
        ordering = ['id']

    def __str__(self):
        return self.email


class Message(models.Model):
    email = models.EmailField(null=False, blank=False, verbose_name='Email')
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    message = models.TextField(null=False, blank=False, verbose_name=_('Message'))

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['id']

    def __str__(self):
        return self.email
