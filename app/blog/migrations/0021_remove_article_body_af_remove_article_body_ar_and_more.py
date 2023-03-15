# Generated by Django 4.0.6 on 2023-02-11 08:56

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_remove_article_body_ru_remove_article_body_uk_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='body_af',
        ),
        migrations.RemoveField(
            model_name='article',
            name='body_ar',
        ),
        migrations.RemoveField(
            model_name='article',
            name='description_af',
        ),
        migrations.RemoveField(
            model_name='article',
            name='description_ar',
        ),
        migrations.RemoveField(
            model_name='article',
            name='intro_af',
        ),
        migrations.RemoveField(
            model_name='article',
            name='intro_ar',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title_af',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title_ar',
        ),
        migrations.AddField(
            model_name='article',
            name='body_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Text'),
        ),
        migrations.AddField(
            model_name='article',
            name='body_uk',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Text'),
        ),
        migrations.AddField(
            model_name='article',
            name='description_ru',
            field=models.CharField(max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='article',
            name='description_uk',
            field=models.CharField(max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='article',
            name='intro_ru',
            field=models.TextField(null=True, verbose_name='Intro'),
        ),
        migrations.AddField(
            model_name='article',
            name='intro_uk',
            field=models.TextField(null=True, verbose_name='Intro'),
        ),
        migrations.AddField(
            model_name='article',
            name='title_ru',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='article',
            name='title_uk',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
    ]