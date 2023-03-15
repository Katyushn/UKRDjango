# Generated by Django 4.0.3 on 2022-07-17 21:12

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('title_en', models.CharField(max_length=250, null=True, verbose_name='Название')),
                ('title_uk', models.CharField(max_length=250, null=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Ссылка')),
                ('description', models.CharField(max_length=250, verbose_name='Описание')),
                ('description_en', models.CharField(max_length=250, null=True, verbose_name='Описание')),
                ('description_uk', models.CharField(max_length=250, null=True, verbose_name='Описание')),
                ('img', models.ImageField(blank=True, null=True, upload_to='post/%Y/%m/', verbose_name='Картинка')),
                ('intro', models.TextField(verbose_name='Вступительный текст')),
                ('intro_en', models.TextField(null=True, verbose_name='Вступительный текст')),
                ('intro_uk', models.TextField(null=True, verbose_name='Вступительный текст')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Основной текст')),
                ('body_en', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Основной текст')),
                ('body_uk', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Основной текст')),
                ('status', models.CharField(choices=[('standard', 'Обычная статья'), ('top', 'Top'), ('banner', 'Banner')], default='standard', max_length=10, verbose_name='Статус')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обнавлено')),
                ('author', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('title_en', models.CharField(max_length=250, null=True, verbose_name='Название')),
                ('title_uk', models.CharField(max_length=250, null=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Ссылка')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обнавлено')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=80, null=True, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('body', models.TextField(verbose_name='Комментарий')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обнавлено')),
                ('active', models.BooleanField(default=True, verbose_name='Включен')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.article', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('created',),
            },
        ),
    ]