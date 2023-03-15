from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from builder.models import Menu
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    STATUS_CHOICES = (
        ('standard', _('Standard')),
        ('top', _('Top')),
        ('banner', _('Banner')),
    )
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(max_length=250, unique=True, null=False, blank=False, verbose_name=_('Link'))
    description = models.CharField(max_length=250, verbose_name=_('Description'))
    author = models.ForeignKey(User, editable=False, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_('Author'))
    category = models.ForeignKey('builder.Category', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Category'))
    template = models.ForeignKey('builder.Template', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Template'))
    img = models.ImageField(upload_to='post/%Y/%m/', null=True, blank=True, verbose_name=_('Images'))
    intro = models.TextField(null=False, blank=False, verbose_name=_('Intro'))
    body = RichTextUploadingField(null=False, blank=False, verbose_name=_('Text'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='standard', verbose_name=_('Status'))
    tags = models.ManyToManyField('builder.Tag', blank=True, verbose_name=_('Tag'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    publish = models.DateTimeField(default=timezone.now, verbose_name=_('Date publish'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    def get_absolute_url(self):
        return reverse('builder:article_product',
                       kwargs={"item_slug": self.category.slug, "item_id": self.category.pk,
                               "value_slug": self.slug, "value_id": self.pk})

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-publish',)

    def delete(self, using=None, keep_parents=False):
        menus = Menu.objects.filter(post=self.id)
        for menu in menus:
            menu.post = None
            menu.save()
        super(Article, self).delete()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Article, null=False, blank=False, on_delete=models.PROTECT, verbose_name=_('Article'))
    name = models.CharField(max_length=80, null=True, blank=True, verbose_name=_('Title'))
    email = models.EmailField(verbose_name='Email')
    body = models.TextField(null=False, blank=False, verbose_name=_('Comment'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ('created',)

    def __str__(self):
        return 'Comment {} width {}'.format(self.name, self.post)

