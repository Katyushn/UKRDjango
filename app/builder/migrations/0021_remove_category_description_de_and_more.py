# Generated by Django 4.0.6 on 2023-01-26 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0020_category_description_de_category_intro_de_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description_de',
        ),
        migrations.RemoveField(
            model_name='category',
            name='intro_de',
        ),
        migrations.RemoveField(
            model_name='category',
            name='title_de',
        ),
        migrations.RemoveField(
            model_name='html',
            name='html_de',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='description_de',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='title_de',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='title_de',
        ),
        migrations.RemoveField(
            model_name='text',
            name='text_de',
        ),
    ]