# Generated by Django 4.0.6 on 2023-02-08 12:39

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
        ('blog', '0018_alter_article_options_alter_comment_options_and_more'),
        ('builder', '0030_remove_category_description_af_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
        migrations.AlterModelOptions(
            name='link',
            options={'verbose_name': 'Link', 'verbose_name_plural': 'Links'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['id'], 'verbose_name': 'Menu', 'verbose_name_plural': 'Menu'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['id'], 'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterModelOptions(
            name='template',
            options={'verbose_name': 'Template', 'verbose_name_plural': 'Templates'},
        ),
        migrations.AlterModelOptions(
            name='text',
            options={'verbose_name': 'Text', 'verbose_name_plural': 'Texts'},
        ),
        migrations.AlterModelOptions(
            name='theme',
            options={'ordering': ('-id',), 'verbose_name': 'Theme', 'verbose_name_plural': 'Themes'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='description_it',
        ),
        migrations.RemoveField(
            model_name='category',
            name='intro_it',
        ),
        migrations.RemoveField(
            model_name='category',
            name='title_it',
        ),
        migrations.RemoveField(
            model_name='html',
            name='html_it',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='description_it',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='title_it',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='title_it',
        ),
        migrations.RemoveField(
            model_name='text',
            name='text_it',
        ),
        migrations.AlterField(
            model_name='category',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_en',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description_uk',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='img',
            field=models.ImageField(blank=True, upload_to='category/%Y/%m/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='intro',
            field=models.TextField(blank=True, verbose_name='Intro'),
        ),
        migrations.AlterField(
            model_name='category',
            name='intro_en',
            field=models.TextField(blank=True, null=True, verbose_name='Intro'),
        ),
        migrations.AlterField(
            model_name='category',
            name='intro_uk',
            field=models.TextField(blank=True, null=True, verbose_name='Intro'),
        ),
        migrations.AlterField(
            model_name='category',
            name='lorem',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Lorems article'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='builder.category', verbose_name='Parent'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='category',
            name='tags',
            field=models.ManyToManyField(blank=True, to='builder.tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='category',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='builder.template', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title_en',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title_uk',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('blog', 'Blog'), ('shop', 'Shop')], default='blog', max_length=10, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='html',
            name='html',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Html'),
        ),
        migrations.AlterField(
            model_name='html',
            name='html_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Html'),
        ),
        migrations.AlterField(
            model_name='html',
            name='html_uk',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Html'),
        ),
        migrations.AlterField(
            model_name='html',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builder.template', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='html',
            name='title',
            field=models.CharField(editable=False, max_length=250, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='template/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='image',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builder.template', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(editable=False, max_length=250, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='languages',
            name='code',
            field=models.CharField(max_length=250, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='languages',
            name='name',
            field=models.SlugField(max_length=250, unique=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='languages',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='link',
            name='link',
            field=models.CharField(default='#', max_length=250, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='link',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builder.template', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='link',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='builder.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='default',
            field=models.BooleanField(default=False, verbose_name='Default pages'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='description_en',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='description_uk',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Ico'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='link',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Link url'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='builder.menu', verbose_name='Parent category'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.article', verbose_name='Article'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shop.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='builder.template', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title_en',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='title_uk',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='type',
            field=models.CharField(choices=[('category', 'Category'), ('article', 'Article'), ('product', 'Product'), ('template', 'Template'), ('link', 'Link')], default='page', max_length=10, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=250, unique=True, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title_en',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title_uk',
            field=models.CharField(max_length=250, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='template',
            name='code',
            field=models.TextField(blank=True, null=True, verbose_name='Html'),
        ),
        migrations.AlterField(
            model_name='template',
            name='default',
            field=models.BooleanField(default=True, verbose_name='Default'),
        ),
        migrations.AlterField(
            model_name='template',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='template',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=250, null=True, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='template',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='builder.theme', verbose_name='Theme'),
        ),
        migrations.AlterField(
            model_name='template',
            name='title',
            field=models.CharField(max_length=250, unique=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='template',
            name='type',
            field=models.CharField(choices=[('page', 'Page'), ('blog', 'Blog'), ('article', 'Article'), ('shop', 'Shop'), ('product', 'Product'), ('block', 'Block'), ('default', 'Default'), ('404', 'Error 404')], max_length=10, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='text',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builder.template', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='text',
            name='text',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='text',
            name='text_en',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='text',
            name='text_uk',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='text',
            name='title',
            field=models.CharField(editable=False, max_length=250, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='template/', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='theme',
            name='title',
            field=models.CharField(editable=False, max_length=250, verbose_name='Title'),
        ),
    ]
