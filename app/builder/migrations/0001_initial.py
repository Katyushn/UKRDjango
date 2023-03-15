# Generated by Django 4.0.3 on 2022-07-17 21:12

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('blog', 'Блог'), ('shop', 'Магазин')], default='page', max_length=10, verbose_name='Тип категории')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('title_en', models.CharField(max_length=250, null=True, verbose_name='Название')),
                ('title_uk', models.CharField(max_length=250, null=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, verbose_name='Ссылка')),
                ('description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('description_en', models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('description_uk', models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('img', models.ImageField(blank=True, upload_to='category/%Y/%m/', verbose_name='Картинка')),
                ('intro', models.TextField(blank=True, verbose_name='Вступительный текст')),
                ('intro_en', models.TextField(blank=True, null=True, verbose_name='Вступительный текст')),
                ('intro_uk', models.TextField(blank=True, null=True, verbose_name='Вступительный текст')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обнавлено')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Html',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Основной текст')),
                ('title', models.CharField(editable=False, max_length=250, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'html',
                'verbose_name_plural': 'html',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='template/', verbose_name='Картинка')),
                ('title', models.CharField(editable=False, max_length=250, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Картинка',
                'verbose_name_plural': 'Картинки',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(default='#', max_length=250, verbose_name='Ссылка')),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='Ссылка')),
                ('description', models.CharField(max_length=250, verbose_name='Описание')),
                ('template', models.CharField(choices=[('admin', 'admin'), ('blog_1.html', 'blog_1.html'), ('default', 'default'), ('_header.html', '_header.html')], max_length=250, verbose_name='Шаблон')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обнавлено')),
            ],
            options={
                'verbose_name': 'Сторінка',
                'verbose_name_plural': 'Сторінки',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Название')),
                ('type', models.CharField(choices=[('page', 'Сторінка'), ('blog', 'Блог'), ('post', 'Стаття'), ('shop', 'Магазин'), ('product', 'Товар'), ('block', 'Блок')], max_length=10, verbose_name='Тип шаблона')),
                ('code', models.TextField(blank=True, null=True, verbose_name='Начальный html')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=250, null=True, verbose_name='Ссылка на шаблон')),
                ('file', models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл')),
                ('default', models.BooleanField(default=True, verbose_name='По умолчанию')),
            ],
            options={
                'verbose_name': 'Шаблон',
                'verbose_name_plural': 'Шаблоны',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(editable=False, max_length=250, verbose_name='Название')),
                ('file', models.FileField(blank=True, null=True, upload_to='template/', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Тема шаблонов',
                'verbose_name_plural': 'Темы шаблонов',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=250, null=True, verbose_name='Название')),
                ('text_en', models.CharField(blank=True, max_length=250, null=True, verbose_name='Название')),
                ('text_uk', models.CharField(blank=True, max_length=250, null=True, verbose_name='Название')),
                ('title', models.CharField(editable=False, max_length=250, verbose_name='Название')),
                ('template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builder.template', verbose_name='Шаблон блога')),
            ],
            options={
                'verbose_name': 'Текст',
                'verbose_name_plural': 'Тексты',
            },
        ),
        migrations.AddField(
            model_name='template',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='builder.theme', verbose_name='Тема шаблона'),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('title_en', models.CharField(max_length=250, null=True, verbose_name='Название')),
                ('title_uk', models.CharField(max_length=250, null=True, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, verbose_name='Ссылка')),
                ('description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('description_en', models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('description_uk', models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание')),
                ('type', models.CharField(choices=[('page', 'Сторінка'), ('category', 'Категория'), ('article', 'Стаття'), ('product', 'Товар'), ('link', 'Ссылка')], default='page', max_length=10, verbose_name='Статус')),
                ('link', models.CharField(blank=True, max_length=250, null=True, verbose_name='Ссылка')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обнавлено')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='builder.category', verbose_name='Лінк на категорію')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='builder.page', verbose_name='Лінк на шаблон')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='builder.menu', verbose_name='Родительская категория')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.article', verbose_name='Лінк на статтю')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
                'ordering': ['id'],
            },
        ),
    ]
