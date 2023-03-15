# Generated by Django 4.0.6 on 2023-02-03 12:03

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0025_remove_category_description_ur_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description_be',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description_uk',
        ),
        migrations.RemoveField(
            model_name='category',
            name='intro_be',
        ),
        migrations.RemoveField(
            model_name='category',
            name='intro_uk',
        ),
        migrations.RemoveField(
            model_name='category',
            name='title_be',
        ),
        migrations.RemoveField(
            model_name='category',
            name='title_uk',
        ),
        migrations.RemoveField(
            model_name='html',
            name='html_be',
        ),
        migrations.RemoveField(
            model_name='html',
            name='html_uk',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='description_be',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='description_uk',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='title_be',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='title_uk',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='title_be',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='title_uk',
        ),
        migrations.RemoveField(
            model_name='text',
            name='text_be',
        ),
        migrations.RemoveField(
            model_name='text',
            name='text_uk',
        ),
        migrations.AddField(
            model_name='category',
            name='description_da',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_dsb',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='category',
            name='intro_da',
            field=models.TextField(blank=True, null=True, verbose_name='Вступительный текст'),
        ),
        migrations.AddField(
            model_name='category',
            name='intro_dsb',
            field=models.TextField(blank=True, null=True, verbose_name='Вступительный текст'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_da',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_dsb',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='html',
            name='html_da',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Основной текст'),
        ),
        migrations.AddField(
            model_name='html',
            name='html_dsb',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Основной текст'),
        ),
        migrations.AddField(
            model_name='menu',
            name='description_da',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='menu',
            name='description_dsb',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='menu',
            name='title_da',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='menu',
            name='title_dsb',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_da',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_dsb',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='text',
            name='text_da',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='text',
            name='text_dsb',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Название'),
        ),
    ]
