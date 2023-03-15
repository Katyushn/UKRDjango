# Generated by Django 4.0.6 on 2023-01-04 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0011_remove_menu_page_alter_menu_type_delete_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='type',
            field=models.CharField(choices=[('category', 'Категория'), ('article', 'Статья'), ('product', 'Товар'), ('template', 'Шаблон'), ('link', 'Ссылка')], default='page', max_length=10, verbose_name='Статус'),
        ),
    ]