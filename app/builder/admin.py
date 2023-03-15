import os
from zipfile import ZipFile
from django.conf import settings
from .models import Menu, Theme, Text, Html, Image, Link, Template, Category, Tag, Languages
from .builder import Builder
from django.contrib import admin
from django.shortcuts import redirect
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from django.db import models
from django.forms import CheckboxSelectMultiple
from blog.models import Article
import random
from lorem_text import lorem
from django.template.defaultfilters import slugify
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.conf.locale import LANG_INFO


class MenuAdmin(TranslationAdmin):
    list_display = ('title', 'slug')
    list_display_links = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


class DraggableTranslationAdmin(TranslationAdmin, DraggableMPTTAdmin):
    class Media:
        media_url = getattr(settings, 'STATIC_URL', '/static')
        js = [media_url + 'admin/js/admin.menu.js', ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "template":
            kwargs["queryset"] = Template.objects.filter(type__in=['page', ])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Menu,
                    DraggableTranslationAdmin,
                    list_display=('tree_actions', 'indented_title',),
                    list_display_links=('indented_title',),)


class CategoryAdmin(TranslationAdmin):
    list_display = ('indented_title', 'parent', 'type')
    list_editable = ('parent',)
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    # hide button delete
    # def has_delete_permission(self, request, obj=None):
    #     if obj is not None and obj.pk == 1:
    #         return False
    #     else:
    #         return True


class DraggableTranslationAdmin(TranslationAdmin, DraggableMPTTAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "template":
            kwargs["queryset"] = Template.objects.filter(type__in=['blog', 'shop'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.type == 'blog' and obj.lorem > 0:
            if len(Article.objects.filter(category=obj)) < 1:
                match_status = ['standard', 'top', 'banner']
                for value in range(obj.lorem):
                    new_title = lorem.words(5).title()
                    if len(Article.objects.filter(slug=slugify(new_title + '-' + str(value)))) < 1:
                        new_img = "https://picsum.photos/800/400/?random&t=" + str(random.randint(1, 10))
                        import requests
                        img_data = requests.get(new_img).content
                        with open(os.path.join(settings.BASE_DIR, 'static/public/random/') + slugify(new_title) + '.jpg', 'wb') as handler:
                            handler.write(img_data)
                        new_status = match_status[random.randint(0, len(match_status) - 1)]
                        new_article = Article(
                            category=obj,
                            title=new_title,
                            description=new_title,
                            slug=slugify(new_title + '-' + str(value)),
                            img='random/' + slugify(new_title) + '.jpg',
                            intro=lorem.paragraphs(1),
                            body='<p>' + lorem.sentence() + '</p>' + '<p>' + lorem.paragraphs(3) + '</p>' + '<p>' + lorem.paragraphs(1) + '</p>',
                            status=new_status,
                        )
                        new_article.save()


admin.site.register(Category,
                    DraggableTranslationAdmin,
                    list_display=('tree_actions', 'indented_title', 'parent', 'type'),
                    list_display_links=('indented_title',), )


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)

    def response_add(self, request, obj, post_url_continue=None):
        with ZipFile(os.path.join(settings.BASE_DIR, 'static' + obj.file.url), 'r') as zipObj:
            zipObj.extractall(os.path.join(settings.BASE_DIR, 'static/'))
        os.unlink(os.path.join(settings.BASE_DIR, 'static' + obj.file.url))
        files = os.listdir(os.path.join(settings.BASE_DIR, 'static/' + obj.title))
        for item in files:
            if '.txt' in item:
                os.unlink(os.path.join(settings.BASE_DIR, 'static/' + obj.title + '/' + item))
        obj.file = ''
        obj.save()

        import json
        from random import randint

        with open(os.path.join(settings.BASE_DIR, 'static/' + obj.title + '/config.json'), 'r') as f:
            my_json_obj = json.load(f)
        my_json_obj['article'] = []
        for i in range(my_json_obj['post']):
            match_status = ['standard', 'top', 'banner']
            new_title = lorem.words(5).title()
            if len(Article.objects.filter(slug=slugify(new_title + '-' + str(i)))) < 1:
                new_img = "https://picsum.photos/800/400/?random&t=" + str(random.randint(1, 10))
                import requests
                img_data = requests.get(new_img).content
                with open(os.path.join(settings.BASE_DIR, 'static/public/random/') + slugify(new_title) + '.jpg','wb') as handler:
                    handler.write(img_data)
                new_status = match_status[random.randint(0, len(match_status) - 1)]
                new_article = Article(
                    title=new_title,
                    description=new_title,
                    slug=slugify(new_title + '-' + str(i)),
                    img='random/' + slugify(new_title) + '.jpg',
                    intro=lorem.paragraphs(1),
                    body='<p>' + lorem.sentence() + '</p>' + '<p>' + lorem.paragraphs(3) + '</p>' + '<p>' + lorem.paragraphs(1) + '</p>',
                    status=new_status,
                )
                new_article.save()
            else:
                new_article = Article.objects.get(slug=slugify(new_title + '-' + str(i)))
            my_json_obj['article'].append(new_article)

        for key in my_json_obj['template']:
            print(os.path.join(settings.BASE_DIR, 'static/' + obj.title + '/' + key['file']))
            file = open(os.path.join(settings.BASE_DIR, 'static/' + obj.title + '/' + key['file']), 'r')
            from django.core.files import File
            with open(os.path.join(settings.BASE_DIR, 'static/' + obj.title + '/' + key['file']), 'r') as f:
                myfile = File(f)
            new_template = Template(
                        theme=obj,
                        title=key['title'],
                        type=key['type'],
                        file=myfile
                    )
            new_template.save()
            if new_template.type == 'default':
                Builder(new_template).template_static()
            Builder(new_template).template()

        def create_new_category(arr, parent=None):
            if len(Category.objects.filter(title=arr['title'])) > 0:
                category = Category.objects.get(title=arr['title'])
                category.type = arr['type']
                category.title = arr['title']
                category.template = Template.objects.get(title=arr['template'])
                category.lorem = arr['lorem']
                category.parent = parent
                category.save()
            else:
                category = Category(
                    type=arr['type'],
                    title=arr['title'],
                    template=Template.objects.get(title=arr['template']),
                    lorem=arr['lorem'],
                    parent=parent,
                )
                category.save()
            parent = category
            if len(arr['subcategory']) > 0:
                for value in arr['subcategory']:
                    create_new_category(value, parent)

        for item in my_json_obj['category']:
            create_new_category(item)

        def create_new_menu(arr, parent=None):
            category = None
            template = None
            post = None
            product = None
            if len(Category.objects.filter(title=arr['category'])) > 0:
                category = Category.objects.get(title=arr['category'])
            if len(Template.objects.filter(title=arr['template'])) > 0:
                template = Template.objects.get(title=arr['template'])
            if len(Article.objects.all()) > 0:
                count = Article.objects.count()
                post = Article.objects.all()[randint(0, count - 1)]

            if len(Menu.objects.filter(title=arr['title'])) > 0:
                menu = Menu.objects.get(title=arr['title'])
                menu.type = arr['type']
                menu.title = arr['title']
                menu.link = arr['link']
                menu.template = template
                menu.category = category
                menu.post = post
                menu.product = product
                menu.default = arr['default']
                menu.parent = parent
                menu.save()
            else:
                menu = Menu(
                    type=arr['type'],
                    title=arr['title'],
                    link=arr['link'],
                    template=template,
                    category=category,
                    post=post,
                    product=product,
                    default=arr['default'],
                    parent=parent,
                )
                menu.save()
            parent = menu
            if len(arr['submenu']) > 0:
                for value in arr['submenu']:
                    create_new_menu(value, parent)

        for item in my_json_obj['menu']:
            create_new_menu(item)

        for item in Category.objects.all():
            if item.lorem > 0:
                for i in range(item.lorem):
                    match_status = ['standard', 'top', 'banner']
                    new_title = lorem.words(5).title()
                    if len(Article.objects.filter(slug=slugify(new_title + '-' + str(i)))) < 1:
                        new_img = "https://picsum.photos/800/400/?random&t=" + str(random.randint(1, 10))
                        import requests
                        img_data = requests.get(new_img).content
                        with open(os.path.join(settings.BASE_DIR, 'static/public/random/') + slugify(new_title) + '.jpg', 'wb') as handler:
                            handler.write(img_data)
                        new_status = match_status[random.randint(0, len(match_status) - 1)]
                        new_article = Article(
                            title=new_title,
                            description=new_title,
                            category=item,
                            slug=slugify(new_title + '-' + str(i)),
                            img='random/' + slugify(new_title) + '.jpg',
                            intro=lorem.paragraphs(1),
                            body='<p>' + lorem.sentence() + '</p>' + '<p>' + lorem.paragraphs(
                                3) + '</p>' + '<p>' + lorem.paragraphs(1) + '</p>',
                            status=new_status,
                        )
                        new_article.save()

        return redirect('/admin/builder/theme/')


class TextInline(TranslationTabularInline):
    model = Text
    raw_id_fields = ['template']
    extra = 0


class HtmlInline(TranslationTabularInline):
    model = Html
    raw_id_fields = ['template']
    extra = 0


class ImageInline(admin.TabularInline):
    model = Image
    raw_id_fields = ['template']
    extra = 0


class LinkInline(admin.TabularInline):
    model = Link
    raw_id_fields = ['template']
    extra = 0


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'theme', 'default')
    inlines = [
        TextInline,
        HtmlInline,
        ImageInline,
        LinkInline,
    ]

    def delete_queryset(self, request, queryset):
        for item in queryset:
            if os.path.exists(os.path.join(settings.BASE_DIR, 'templates/' + item.slug)):
                os.unlink(os.path.join(settings.BASE_DIR, 'templates/' + item.slug))
            menus = Menu.objects.filter(template=item.id)
            for menu in menus:
                menu.template = None
                menu.save()
            item.delete()

    def response_add(self, request, obj, post_url_continue=None):
        if obj.type == 'default':
            Builder(obj).template_static()
        Builder(obj).template()
        return redirect('/admin/builder/template/')

    def response_change(self, request, obj):
        if obj.type == 'default':
            Builder(obj).template_static()
        Builder(obj).template()
        return redirect('/admin/builder/template/')

    class Media:
        media_url = getattr(settings, 'STATIC_URL', '/static')
        js = [media_url + 'admin/js/admin.template.js', ]


@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    list_display = ('title', 'created')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'status')

    actions = ['languages_list', ]

    def languages_list(self, request, queryset):
        lang_list = "LANGUAGES = (('en', _('English')), "
        for item in Languages.objects.all():
            item.status = False
            item.save()
        for item in queryset:
            if item.code != 'en':
                item.status = True
                item.save()
                new_lang = "('" + item.code + "', _('" + item.name + "')), "
                lang_list += new_lang
        if len(Languages.objects.filter(code='en')) > 0:
            en = Languages.objects.get(code='en')
            en.status = True
            en.save()
        lang_list += ")"
        test = open(os.path.join(settings.BASE_DIR, 'app/settings.py'), 'a')
        test.write("\r" + lang_list)
        test.close()
        return redirect('/en/admin/builder/languages/dbup')

    languages_list.short_description = _("Create a new language pack")

    '''custom button'''
    change_list_template = 'admin/lang_change_list.html'

    def db_update(self, request):
        self.message_user(request, 'Language list change anp update data base')
        os.system('cmd /c "..\\venv\\Scripts\\python.exe manage.py makemigrations --no-input"')
        os.system('cmd /c "..\\venv\\Scripts\\python.exe manage.py migrate --no-input"')
        os.system('cmd /c "..\\venv\\Scripts\\python.exe manage.py update_translation_fields"')
        for item in Languages.objects.filter(status=True):
            if item.code != 'en':
                new_locale_file = 'cmd /c "..\\venv\\Scripts\\python.exe manage.py makemessages -l ' + item.code + ' --ignore env"'
                db_locale_db = 'cmd /c "..\\venv\\Scripts\\python.exe manage.py update_translation_fields --language ' + item.code + '"'
                os.system(db_locale_db)
                os.system(new_locale_file)
        return redirect('/en/admin/builder/languages/')

    def lang_insert(self, request):
        self.message_user(request, 'Language list ')
        for item in LANG_INFO:
            for value in LANG_INFO[item]:
                if value == 'name':
                    if len(Languages.objects.filter(code=item)) < 1:
                        new_lan = Languages(
                            code=item,
                            name=LANG_INFO[item][value],
                        )
                        new_lan.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_urls(self):
        urls = super(LanguagesAdmin, self).get_urls()
        custom_urls = [
            path('langins/', self.lang_insert),
            path('dbup/', self.db_update),
        ]
        return custom_urls + urls

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
