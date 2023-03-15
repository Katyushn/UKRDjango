# Generated by Django 4.0.6 on 2023-02-03 08:07

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0022_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description_uz',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='category',
            name='intro_uz',
            field=models.TextField(blank=True, null=True, verbose_name='Вступительный текст'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_uz',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='html',
            name='html_uz',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Основной текст'),
        ),
        migrations.AddField(
            model_name='menu',
            name='description_uz',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='menu',
            name='title_uz',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_uz',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='text',
            name='text_uz',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Название'),
        ),
    ]