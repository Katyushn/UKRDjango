# Generated by Django 4.0.6 on 2023-01-26 14:33

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_delete_tag_alter_article_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='body_de',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Основной текст'),
        ),
        migrations.AddField(
            model_name='article',
            name='description_de',
            field=models.CharField(max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='article',
            name='intro_de',
            field=models.TextField(null=True, verbose_name='Вступительный текст'),
        ),
        migrations.AddField(
            model_name='article',
            name='title_de',
            field=models.CharField(max_length=250, null=True, verbose_name='Название'),
        ),
    ]
