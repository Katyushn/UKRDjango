# Generated by Django 4.0.6 on 2023-02-03 08:07

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_article_title_alter_article_title_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='body_uz',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Основной текст'),
        ),
        migrations.AddField(
            model_name='article',
            name='description_uz',
            field=models.CharField(max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='article',
            name='intro_uz',
            field=models.TextField(null=True, verbose_name='Вступительный текст'),
        ),
        migrations.AddField(
            model_name='article',
            name='title_uz',
            field=models.CharField(max_length=250, null=True, verbose_name='Назва'),
        ),
    ]