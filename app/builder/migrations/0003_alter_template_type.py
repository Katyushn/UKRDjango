# Generated by Django 4.0.3 on 2022-07-18 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='type',
            field=models.CharField(choices=[('page', 'Сторінка'), ('blog', 'Блог'), ('article', 'Стаття'), ('shop', 'Магазин'), ('product', 'Товар'), ('block', 'Блок')], max_length=10, verbose_name='Тип шаблона'),
        ),
    ]
