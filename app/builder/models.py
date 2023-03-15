from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel
import os
from django.utils.text import slugify
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Menu(MPTTModel):
    TYPE_CHOICES = (
        ('category', _('Category')),
        ('article', _('Article')),
        ('product', _('Product')),
        ('template', _('Template')),
        ('link', _('Link')),
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True, verbose_name=_('Parent category'))
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(max_length=250, null=True, blank=True, verbose_name=_('Link'))
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Description'))
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='page', verbose_name=_('Status'))
    template = models.ForeignKey('builder.Template', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_('Template'))
    category = models.ForeignKey('builder.Category', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_('Category'))
    post = models.ForeignKey('blog.Article', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_('Article'))
    product = models.ForeignKey('shop.Product', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=_('Product'))
    link = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Link url'))
    icon = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Ico'))
    default = models.BooleanField(default=False, verbose_name=_('Default pages'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')
        ordering = ['id']

    class MPTTMeta:
        order_insertion_by = ['id']

    def get_absolute_url(self):
        if self.default:
            return '/'
        else:
            if self.type == 'link':
                return self.link
            else:
                return reverse('builder:menu', kwargs={"item_slug": self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.default:
            query_true_default = Menu.objects.filter(default=True)
            for item in query_true_default:
                item.default = False
                item.save()
        super().save(*args, **kwargs)

    def clean(self):
        if self.type == 'category' and self.category is None:
            raise ValidationError("Category is not None")
        if self.type == 'article' and self.post is None:
            raise ValidationError("Article is not None")
        if self.type == 'product' and self.product is None:
            raise ValidationError("Product is not None")
        if self.type == 'template' and self.template is None:
            raise ValidationError("Template is not None")
        if self.type == 'link' and self.link is None:
            raise ValidationError("Link is not None")
        if self.type == 'link' and self.default:
            raise ValidationError("Default menu don`t type a link")


class Category(MPTTModel):
    TYPE_CHOICES = (
        ('blog', _('Blog')),
        ('shop', _('Shop')),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='blog', verbose_name=_('Type'))
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', null=True, blank=True, verbose_name=_('Parent'))
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(max_length=250, null=True, blank=True, verbose_name=_('Link'))
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Description'))
    img = models.ImageField(upload_to='category/%Y/%m/', blank=True, verbose_name=_('Image'))
    intro = models.TextField(blank=True, verbose_name=_('Intro'))
    template = models.ForeignKey('builder.Template', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_('Template'))
    tags = models.ManyToManyField('builder.Tag', blank=True, verbose_name=_('Tags'))
    lorem = models.IntegerField(default=0, null=True, blank=True, verbose_name=_('Lorems article'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class MPTTMeta:
        order_insertion_by = ['id']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('builder:page_blog_shop', kwargs={"item_slug": self.slug, "item_id": self.pk})

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        menus = Menu.objects.filter(category=self.id)
        for menu in menus:
            menu.category = None
            menu.save()
        from django.apps import apps
        Article = apps.get_model('blog', 'Article')
        articles = Article.objects.filter(category=self.id)
        print(articles)
        for article in articles:
            article.category = None
            article.save()
        super(Category, self).delete()

    def save(self, *args, **kwargs):
        if self.template:
            if self.type != self.template.type:
                self.template = None
        if self.parent:
            self.type = self.parent.type
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

        def type_recursive(my_parent):
            children = Category.objects.filter(parent=my_parent)
            if len(children) > 0:
                for item in children:
                    item.type = self.type
                    item.save()
                    type_recursive(item.id)

        type_recursive(self.id)


class Theme(models.Model):
    title = models.CharField(max_length=250, editable=False, verbose_name=_('Title'))
    file = models.FileField(upload_to='template/', null=True, blank=True, verbose_name=_('File'))

    class Meta:
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')
        ordering = ('-id',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if Theme.objects.filter(title=self.file):
            for item in Theme.objects.filter(title=self.file):
                item.delete()
        if self.title == '':
            self.title = str(self.file).replace('.zip', '')
        super(Theme, self).save(*args, **kwargs)


class Template(models.Model):
    TYPE_CHOICES = (
        ('page', _('Page')),
        ('blog', _('Blog')),
        ('article', _('Article')),
        ('shop', _('Shop')),
        ('product', _('Product')),
        ('block', _('Block')),
        ('default', _('Default')),
        ('404', _('Error 404')),
    )
    theme = models.ForeignKey(Theme, null=False, blank=False, on_delete=models.PROTECT, verbose_name=_('Theme'))
    title = models.CharField(max_length=250, null=False, blank=False, unique=True, verbose_name=_('Title'))
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=False, blank=False, verbose_name=_('Type'))
    code = models.TextField(null=True, blank=True, verbose_name=_('Html'))
    slug = models.SlugField(max_length=250, editable=False, null=True, blank=True, verbose_name=_('Link'))
    file = models.FileField(upload_to='', null=True, blank=True, verbose_name=_('File'))
    default = models.BooleanField(default=True, verbose_name=_('Default'))

    class Meta:
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self):
        return '{}'.format(self.title)

    def delete(self, using=None, keep_parents=False):
        if os.path.exists(os.path.join(settings.BASE_DIR, 'templates/' + self.slug)):
            os.unlink(os.path.join(settings.BASE_DIR, 'templates/' + self.slug))
        menus = Menu.objects.filter(template=self.id)
        for menu in menus:
            menu.template = None
            menu.save()
        super(Template, self).delete()

    def save(self, *args, **kwargs):
        if self.default:
            if self.type != 'block':
                query_true_default = Template.objects.filter(type=self.type, default=True)
                for item in query_true_default:
                    item.default = False
                    item.save()
        if self.file:
            html_file = self.file.open(mode='rb').readlines()
            html_str = ''
            for item in html_file:
                html_str += item.decode("utf-8")
            self.code = html_str
            self.file = ''
        if not self.slug:
            if self.type != 'block':
                self.slug = str(self.type) + '_'
                super().save(*args, **kwargs)
                self.slug = self.slug + str(self.pk) + '.html'
        super().save(*args, **kwargs)


class Text(models.Model):
    text = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Text'))
    title = models.CharField(max_length=250, editable=False, null=False, blank=False, verbose_name=_('Title'))
    template = models.ForeignKey(Template, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Template'))

    class Meta:
        verbose_name = _('Text')
        verbose_name_plural = _('Texts')


class Html(models.Model):
    html = RichTextUploadingField(null=True, blank=True, verbose_name=_('Html'))
    title = models.CharField(max_length=250, editable=False, null=False, blank=False, verbose_name=_('Title'))
    template = models.ForeignKey(Template, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Template'))

    class Meta:
        verbose_name = 'html'
        verbose_name_plural = 'html'


class Image(models.Model):
    img = models.ImageField(upload_to='template/', null=True, blank=True, verbose_name=_('Image'))
    title = models.CharField(max_length=250, editable=False, null=False, blank=False, verbose_name=_('Title'))
    template = models.ForeignKey(Template, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Template'))

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class Link(models.Model):
    link = models.CharField(max_length=250, null=False, blank=False, default='#', verbose_name=_('Link'))
    title = models.CharField(max_length=250, null=False, blank=False, verbose_name=_('Title'))
    template = models.ForeignKey(Template, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Template'))

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')


class Tag(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(max_length=250, unique=True, null=False, blank=False, verbose_name=_('Link'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('builder:blog_tag', kwargs={"item_slug": self.slug, "item_id": self.pk})

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['id']


class Languages(models.Model):
    code = models.CharField(max_length=250, verbose_name=_('Code'))
    name = models.SlugField(max_length=250, unique=True, null=False, blank=False, verbose_name=_('Country'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['id']
