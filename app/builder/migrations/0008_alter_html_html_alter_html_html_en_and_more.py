# Generated by Django 4.0.6 on 2022-12-27 15:41

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0007_alter_page_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='html',
            name='html',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Основной текст'),
        ),
        migrations.AlterField(
            model_name='html',
            name='html_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Основной текст'),
        ),
        migrations.AlterField(
            model_name='html',
            name='html_uk',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Основной текст'),
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=models.CharField(choices=[('default_16.html', 'default_16.html'), ('_footer.html', '_footer.html'), ('_header.html', '_header.html'), ('admin', 'admin'), ('default', 'default'), ('default_login.html', 'default_login.html'), ('default_password_change.html', 'default_password_change.html'), ('default_profile.html', 'default_profile.html'), ('default_profile_edit.html', 'default_profile_edit.html'), ('default_register.html', 'default_register.html'), ('default_share.html', 'default_share.html'), ('default_404.html', 'default_404.html'), ('header.html', 'header.html'), ('breadcrumb.html', 'breadcrumb.html'), ('footer.html', 'footer.html'), ('blog_132.html', 'blog_132.html'), ('blog_135.html', 'blog_135.html'), ('blog_138.html', 'blog_138.html'), ('blog_141.html', 'blog_141.html'), ('blog_144.html', 'blog_144.html')], max_length=250, verbose_name='Шаблон'),
        ),
    ]
