from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files import File
from django.template.defaultfilters import slugify
from .models import Template, Menu, Text, Html, Image, Link, Category
from blog.models import Article
import hashlib
import os
import re
import random
import textwrap
from django.utils import timezone
from lorem_text import lorem


class Builder:

    def __init__(self, obj):
        self.obj = obj
        self.txt_model = Text
        self.html_model = Html
        self.img_model = Image
        self.link_model = Link

    def template(self):
        template_name = self.obj.theme.title
        soup = BeautifulSoup(self.obj.code, 'html.parser')

        """ block """
        for position, item in enumerate(soup.find_all(attrs={"data-django-block": True})):
            slug = str(item['data-django-block']) + '.html'
            if len(Template.objects.filter(slug=slug)) < 1:
                del item['data-django-block']
                new_block = Template(code=str(item), title=slug.replace('.html', ''), type='block', slug=slug,
                                     theme=self.obj.theme)
                new_block.save()
                Builder(new_block).template()
            item.replace_with("{% include '" + slug + "' %}")

        """ main """
        if soup.select('[data-django="main"]'):
            soup.select_one('[data-django="main"]').string = '{% include main %}'

        """ meta and title """
        if soup.select('title'):
            soup.title.string = '{{ title }}'
        for tag in soup.find_all(attrs={"data-django": "title"}):
            tag.string = '{{ title }}'

        if soup.select('meta[name="description"]'):
            soup.select_one('meta[name="description"]')['content'] = '{{ description }}'
        else:
            if soup.select('head'):
                new_tag = soup.new_tag("meta")
                new_tag['name'] = "description"
                new_tag['content'] = "{{ description }}"
                soup.head.append(new_tag)

        if soup.select('meta[property="og:title"]'):
            soup.select_one('meta[property="og:title"]')['content'] = '{{ title }}'
        else:
            if soup.select('head'):
                new_tag = soup.new_tag("meta")
                new_tag['property'] = "og:title"
                new_tag['content'] = "{{ title }}"
                soup.head.append(new_tag)

        if soup.select('meta[property="og:description"]'):
            soup.select_one('meta[property="og:description"]')['content'] = '{{ description }}'
        else:
            if soup.select('head'):
                new_tag = soup.new_tag("meta")
                new_tag['property'] = "og:description"
                new_tag['content'] = "{{ description }}"
                soup.head.append(new_tag)

        if soup.select('meta[property="og:type"]'):
            soup.select_one('meta[property="og:type"]')['content'] = 'blog'
        else:
            if soup.select('head'):
                new_tag = soup.new_tag("meta")
                new_tag['property'] = "og:type"
                new_tag['content'] = "blog"
                soup.head.append(new_tag)

        if soup.select('meta[property="og:url"]'):
            soup.select_one('meta[property="og:url"]')['content'] = '{{ request.path }}'
        else:
            if soup.select('head'):
                new_tag = soup.new_tag("meta")
                new_tag['property'] = "og:url"
                new_tag['content'] = "{{request.path}}"
                soup.head.append(new_tag)

        if soup.select('meta[property="og:image"]'):
            soup.select_one('meta[property="og:image"]')['content'] = '{{ category.img }}'
        else:
            if soup.select('head'):
                new_tag = soup.new_tag("meta")
                new_tag['property'] = "og:image"
                new_tag['content'] = "{{ category.img }}"
                soup.head.append(new_tag)

        """ image """
        for tag in soup.find_all():
            for attr in tag.attrs:
                if ('.jpg' in tag[attr] or '.png' in tag[attr] or '.ico' in tag[attr]) and tag.name != 'link':
                    name_img = ''
                    title_img = ''
                    file_img = ''
                    if attr != 'style':
                        name_img = os.path.basename(
                            os.path.join(settings.BASE_DIR, 'static/' + template_name + '/' + tag[attr]))
                        file_img = File(
                            open(os.path.join(settings.BASE_DIR, 'static/' + template_name + '/' + tag[attr]), 'rb'))
                        title_img = tag[attr][:-4].translate({ord(i): None for i in '.,-_/|!'})
                        tag[attr] = '{{ img_' + title_img + '_' + str(self.obj.id) + '.img.url }}'
                    else:
                        if ';' in tag[attr]:
                            arr = tag[attr].split(';')
                            for value in arr:
                                if 'background-image' in value:
                                    name_img = os.path.basename(os.path.join(settings.BASE_DIR,
                                                                             'static/' + template_name + '/' + value.replace(
                                                                                 ':', '').replace('background-image',
                                                                                                  '').replace(
                                                                                 ' ', '').replace('url(\'', '').replace(
                                                                                 ')', '')))
                                    file_img = File(open(os.path.join(settings.BASE_DIR,
                                                                      'static/' + template_name + '/' + value.replace(
                                                                          ':', '').replace('background-image',
                                                                                           '').replace(' ',
                                                                                                       '').replace(
                                                                          'url(\'', '').replace(')', '')), 'rb'))
                                    title_img = name_img[:-4].translate({ord(i): None for i in '.,-_/|!'})
                                    value.replace(' ', '').replace('url(\'',
                                                                   'url({{ img_' + title_img + '_' + str(self.obj.id) + '.img.url').replace(')',
                                                                                                                   ' }})')
                        else:
                            if 'background-image' in tag[attr]:
                                name_img = os.path.basename(os.path.join(settings.BASE_DIR,
                                                                         'static/' + template_name + '/' + tag[
                                                                             attr].replace(':', '').replace(
                                                                             'background-image', '').replace(
                                                                             ' ', 'url(\'', '').replace(')', '')))
                                file_img = File(open(os.path.join(settings.BASE_DIR,
                                                                  'static/' + template_name + '/' + tag[attr].replace(
                                                                      ':', '').replace('background-image', '').replace(
                                                                      ' ',
                                                                      'url(\'',
                                                                      '').replace(
                                                                      ')', '')), 'rb'))
                                title_img = name_img[:-4].translate({ord(i): None for i in '.,-_/|!'})
                                tag[attr] = tag[attr].replace(' ', '').replace('url(\'',
                                                                               'url({{ img_' + title_img + '_' + str(self.obj.id) + '.img.url').replace(
                                    ')', ' }})')
                    if len(self.img_model.objects.filter(title=title_img, template=self.obj)) < 1:
                        new_img = self.img_model(title=title_img, template=self.obj)
                        new_img.save()
                        new_img.img.save(name_img, file_img)

        """ css """
        if soup.select('head'):
            for tag in soup.find_all("link"):
                if tag.get('href') is not None and tag.get('href').find('http') < 0 and tag.get('href').find('//') < 0:
                    tag['href'] = '{% static \'/' + template_name + '/' + tag.get('href') + '\' %}'
            style = []
            for tag in soup.find_all("link", rel="stylesheet"):
                style.append(tag)
            soup.head.append('{% compress css %}')
            for item in style:
                soup.head.append(item)
            soup.head.append('{% endcompress %}')

        """ script """
        if soup.select('script'):
            script = []
            for tag in soup.find_all("script"):
                if tag.get('src') is not None:
                    if 'http' in tag['src']:
                        tag['src'] = tag.get('src')
                    else:
                        tag['src'] = '{% static \'/' + template_name + '/' + tag.get('src') + '\' %}'
                    script.append(tag)
            if len(script) > 0:
                if soup.select('body'):
                    soup.body.append('{% compress js %}')
                    for item in script:
                        soup.body.append(item)
                else:
                    soup.append('{% compress js %}')
                    for item in script:
                        soup.append(item)
                if soup.select('body'):
                    soup.body.append('{% endcompress %}')
                else:
                    soup.append('{% endcompress %}')

        """ link """
        if soup.select('a'):
            for tag in soup.find_all('a'):
                if tag.has_attr('data-django-link'):
                    if len(self.link_model.objects.filter(title=tag['data-django-link'], template=self.obj)) < 1:
                        new_link = self.link_model(link='#', title=tag['data-django-link'], template=self.obj)
                        new_link.save()
                    tag['href'] = '{{ link_' + str(tag['data-django-link']) + '_' + str(self.obj.id) + '.link }}'
                # else:
                #     new_link = LinkCategoryTemplate(link='#', title='link_', template=obj)
                #     new_link.save()
                #     up_new_link = new_link
                #     up_new_link.title = new_link.title + str(new_link.id)
                #     up_new_link.save()
                #     tag['href'] = '{{ link_' + up_new_link.title + '.link }}'

        """ messages """
        if soup.select('[data-django=messages]'):
            soup.select_one('[data-django=messages]').append(BeautifulSoup("""
                        {% if messages %}
                            {% for message in messages %}
                                {% if message.tags == 'error' %}
                                    <div class="container" style="margin-top: 1rem;color: #721c24;background-color: #f8d7da;position: relative;padding: 0.75rem 1.25rem;margin-bottom: 1rem;border: #f5c6cb 1px solid;border-radius: 0.25rem;">
                                        {{ message }}
                                    </div>
                                {% else %}
                                    <div class="container" style="margin-top: 1rem;color: #155724;background-color: #d4edda;position: relative;padding: 0.75rem 1.25rem;margin-bottom: 1rem;border: #c3e6cb 1px solid;border-radius: 0.25rem;">
                                        {{ message }}
                                    </div>
                                {% endif %}
                            {% endfor %}
                        {% endif %}
                    """, 'html.parser'))

        """ category """
        for item in soup.find_all('ul', attrs={"data-django-new-category-blog": True}):
            if len(Category.objects.filter(slug=slugify(item['data-django-new-category-blog']), parent=None)) < 1:
                category_ins = Category(title=item['data-django-new-category-blog'].title(),
                                        slug=slugify(item['data-django-new-category-blog']),
                                        type='blog')
                category_ins.save()
                li = item.findChildren('li', recursive=False)
                for parent_li in li:
                    if parent_li.select('a'):
                        category_ins_li = Category(parent=category_ins, title=parent_li.select_one('a').string,
                                                   slug=slugify(parent_li.select_one('a').string), type='blog')
                        category_ins_li.save()
                    if parent_li.select('ul'):
                        children_ul = parent_li.select_one('ul')
                        for children_li in children_ul.findChildren('li', recursive=False):
                            category_ins_li_li = Category(parent=category_ins_li,
                                                          title=children_li.select_one('a').string,
                                                          slug=slugify(children_li.select_one('a').string), type='blog')
                            category_ins_li_li.save()
        for item in soup.find_all('ul', attrs={"data-django-new-category-shop": True}):
            if len(Category.objects.filter(slug=slugify(item['data-django-new-category-shop']), parent=None)) < 1:
                category_ins = Category(title=item['data-django-new-category-shop'].title(),
                                        slug=slugify(item['data-django-new-category-shop']),
                                        type='shop')
                category_ins.save()
                li = item.findChildren('li', recursive=False)
                for parent_li in li:
                    if parent_li.select('a'):
                        category_ins_li = Category(parent=category_ins, title=parent_li.select_one('a').string,
                                                   slug=slugify(parent_li.select_one('a').string), type='shop')
                        category_ins_li.save()
                    if parent_li.select('ul'):
                        children_ul = parent_li.select_one('ul')
                        for children_li in children_ul.findChildren('li', recursive=False):
                            category_ins_li_li = Category(parent=category_ins_li,
                                                          title=children_li.select_one('a').string,
                                                          slug=slugify(children_li.select_one('a').string), type='shop')
                            category_ins_li_li.save()
        for item in soup.find_all('ul', attrs={"data-django-category": True}):
            category_name = item['data-django-category']
            if item.select('ul'):
                children_ul = item.select_one('ul')
                children_ul.string = '{{ children }}'
            else:
                children_ul = BeautifulSoup('''<ul>{{ children }}</ul>''', 'html.parser')
            parent_li = item.select_one('li')
            parent_li.select_one('a')['href'] = "{{ node.get_absolute_url }}"
            parent_li.select_one('a').string = "{{ node.title }}"
            if parent_li.select_one('a').has_attr('class'):
                parent_li.select_one('a')['class'].replace('activ', '')
                parent_li.select_one('a')['class'] += " {% if node.id == category.id %} activ {% endif %}"
            else:
                parent_li.select_one('a')['class'] = " {% if node.id == category.id %} activ {% endif %}"
            for tmp in item.findChildren('li', recursive=False):
                tmp.replace_with('')
            parent_li.append(
                BeautifulSoup('''{% if not node.is_leaf_node %} ''' + str(children_ul) + ''' {% endif %}''',
                              'html.parser'))

            item.append(BeautifulSoup('''{% recursetree category_''' + category_name + ''' %}''' + str(
                parent_li) + '''{% endrecursetree %}''', 'html.parser'))

        # for item in soup.find_all(attrs={"data-django": "module-blog-category"}):
        #     for value in item.findChildren(recursive=False):
        #         value.replace_with('')
        #     item.append(BeautifulSoup('''
        #                 <ul>
        #                     {% for item in menu_blog_categories %}
        #                         {% recursetree item %}
        #                             <li>
        #                                 <a class="{% if node.blog.id == category.id %} activ {% endif %}" href="{{ node.get_absolute_url }}">
        #                                     {{ node.title }}
        #                                 </a>
        #                                 {% if not node.is_leaf_node %}
        #                                     <ul>
        #                                         {{ children }}
        #                                     </ul>
        #                                 {% endif %}
        #                             </li>
        #                         {% endrecursetree %}
        #                     {% endfor %}
        #                 </ul>
        #             ''', 'html.parser'))

        """ menu """
        for item in soup.find_all('ul', attrs={"data-django-new-menu": True}):
            if len(Menu.objects.filter(slug=slugify(item['data-django-new-menu']), parent=None)) < 1:
                menu_ins = Menu(title=item['data-django-new-menu'], slug=slugify(item['data-django-new-menu']),
                                type='link', link='#')
                menu_ins.save()
                li = item.findChildren('li', recursive=False)
                for parent_li in li:
                    if parent_li.select('a'):
                        if parent_li.select_one('a').find('i'):
                            menu_tag_i = parent_li.select_one('a').find('i')
                            parent_li.select_one('a').find('i').replace_with('')
                            menu_str = parent_li.select_one('a').text.strip()
                        else:
                            menu_tag_i = ''
                            menu_str = parent_li.select_one('a').text
                        menu_ins_li = Menu(parent=menu_ins, title=menu_str, slug=slugify(menu_str), icon=str(menu_tag_i), type='link', link='#')
                        menu_ins_li.save()
                    if parent_li.select('ul'):
                        children_ul = parent_li.select_one('ul')
                        for children_li in children_ul.findChildren('li', recursive=False):
                            if children_li.select_one('a').find('i'):
                                menu_tag_i = children_li.select_one('a').find('i')
                                children_li.select_one('a').find('i').replace_with('')
                                menu_str = children_li.select_one('a').text.strip()
                            else:
                                menu_tag_i = ''
                                menu_str = children_li.select_one('a').text
                            menu_ins_li_li = Menu(parent=menu_ins_li, title=menu_str, slug=slugify(menu_str), icon=str(menu_tag_i), type='link',
                                                  link='#')
                            menu_ins_li_li.save()

        for item in soup.find_all('ul', attrs={"data-django-menu": True}):
            menu_name = item['data-django-menu']
            if item.select('ul'):
                children_ul = item.select_one('ul')
                children_ul.string = '{{ children }}'
            else:
                children_ul = BeautifulSoup('''<ul>{{ children }}</ul>''', 'html.parser')
            parent_li = item.select_one('li')
            if parent_li.has_attr('class'):
                parent_li['class'] += "{% if node.get_absolute_url == request.path %} active {% endif %}"
            else:
                parent_li['class'] = "{% if node.get_absolute_url == request.path %} active {% endif %}"
            if parent_li.select_one('a').has_attr('class'):
                parent_li.select_one('a')['class'] += "{% if node.get_absolute_url == request.path %} active {% endif %}"
            else:
                parent_li.select_one('a')['class'] = "{% if node.get_absolute_url == request.path %} active {% endif %}"
            parent_li.select_one('a')['href'] = "{{ node.get_absolute_url }}"
            parent_li.select_one('a').string = "{{ node.title }} {% if node.icon != None %}{{ node.icon | safe }}{% endif %}"
            for tmp in item.findChildren('li', recursive=False):
                tmp.replace_with('')
            parent_li.append(
                BeautifulSoup('''{% if not node.is_leaf_node %} ''' + str(children_ul) + ''' {% endif %}''',
                              'html.parser'))

            item.append(BeautifulSoup(
                '''{% recursetree menu_''' + menu_name + ''' %}''' + str(parent_li) + '''{% endrecursetree %}''',
                'html.parser'))

        """ language """
        language_blocks = soup.find_all(attrs={"data-django": "language"})
        for language in language_blocks:
            # if language.name == 'ul':
            #     new_language_ul = soup.new_tag("ul")
            #     new_language_li = soup.new_tag("li")
            #     new_language_a = soup.new_tag("a")
            #     new_language_icon = ':'
            #     if language.select('i', attrs={"string": False}):
            #         new_language_icon = language.select_one('i')
            #     if language.select('span', attrs={"string": False}):
            #         new_language_icon = language.select_one('span')
            #     if language.findChildren('ul')[0].get('class') is not None:
            #         new_language_ul["class"] = language.findChildren('ul')[0]['class']
            #     if language.findChildren('li')[0].get('class') is not None:
            #         new_language_li["class"] = language.findChildren('li')[0]['class']
            #     if language.findChildren('a')[0].get('class') is not None:
            #         new_language_a["class"] = str(language.findChildren('a')[0][
            #                                           'class']) + '{% if language.code == LANGUAGE_CODE %} selected {% endif %}'
            #     else:
            #         new_language_a["class"] = '{% if language.code == LANGUAGE_CODE %} selected {% endif %}'
            #     new_language_a["href"] = '/{{ language.code }}'
            #     new_language_a.string = '{{ language.name_local }}'
            #     language.clear()
            #     new_language_li.append(new_language_a)
            #     new_language_ul.append(
            #         BeautifulSoup('''{% for language in languages %}''' + str(new_language_li) + '''{% endfor %}''',
            #                       'html.parser'))
            #     language.append(BeautifulSoup('''
            #                 {% get_current_language as LANGUAGE_CODE %}
            #                 {% get_available_languages as LANGUAGES %}
            #                 {% get_language_info_list for LANGUAGES as languages %}
            #                 <div>{% for language in languages %}{% if language.code == LANGUAGE_CODE %}
            #                 {{ language.name_local }}{% endif %}{% endfor %} ''' + str(new_language_icon) + '''</div>
            #              ''' + str(new_language_ul), 'html.parser'))
            for value in language.findChildren(recursive=False):
                value.replace_with('')
            language.append(
                    BeautifulSoup('''
                        {% get_current_language as LANGUAGE_CODE %}
                           <form action="{% url 'account:lang' %}" method="post">
                               {% csrf_token %}
                               <label style="position: relative;">
                                   <select name="lang" id="" onchange="this.form.submit()" style="padding: 3px 10px;background: #eee;border: none;outline: none;display: inline-block;-webkit-appearance: none;-moz-appearance: none;appearance: none;cursor: pointer;">
                                       {% get_current_language as LANGUAGE_CODE %}
                                       {% get_available_languages as LANGUAGES %}
                                       {% get_language_info_list for LANGUAGES as languages %}
                                       {% for language in languages %}
                                           {% if language.code == LANGUAGE_CODE %}
                                               <option selected value="{{ language.code }}">{{ language.name_local }}</option>
                                           {% else %}
                                               <option value="{{ language.code }}">{{ language.name_local }}</option>
                                           {% endif %}
                                       {% endfor %}
                                   </select>
                               </label>
                           </form>
                    ''', 'html.parser'))

        """ auth """
        for tag in soup.find_all(attrs={"data-django": "login"}):
            tag.string = str(tag.select_one('i')) + """
                    {% if request.user.is_authenticated %}
                        {{ txt_wellcom.text }}, <a style="display: inline;" href="{% url 'account:profile' %}">{{ user.username }}</a> |
                            <a style="display: inline;" href="{% url 'account:logout' %}">{{ txt_exit.text }}</a>
                        {% else %}
                            <a style="display: inline;" href="{% url 'account:register' %}">{{ txt_register.text }}</a> |
                            <a style="display: inline;" href="{% url 'account:login' %}">{{ txt_enter.text }}</a>
                        {% endif %}
                    """
        if soup.select('[data-django="login"]'):
            match = ['wellcom', 'exit', 'register', 'enter']
            for item in match:
                if len(self.txt_model.objects.filter(title=item, template=self.obj)) < 1:
                    text = self.txt_model(text=str.capitalize(item), title=item, template=self.obj)
                    text.save()

        """ cart """
        if soup.select('[data-django="cart-link"]'):
            for item in soup.find_all(attrs={"data-django": "cart-link"}):
                item['href'] = '{% url "cart:detail" %}'
        if soup.select('[data-django="cart-item"]'):
            for item in soup.find_all(attrs={"data-django": "cart-item"}):
                item.string = '{% with total_items=cart|length %}{% if cart.cart|length > 0 %}{{ total_items }}{% else %}0{% endif %}{% endwith %}'
        if soup.select('[data-django="cart-price"]'):
            for item in soup.find_all(attrs={"data-django": "cart-price"}):
                item.string = '{% with total_items=cart|length %}{% if cart.cart|length > 0 %}{{ cart.get_total_price }}{% else %}0{% endif %}{% endwith %}'

        if soup.select('[data-django="cart-wishes-link"]'):
            for item in soup.find_all(attrs={"data-django": "cart-wishes-link"}):
                item['href'] = '{% url "cart:wishes" %}'
        if soup.select('[data-django="cart-wishes-item"]'):
            for item in soup.find_all(attrs={"data-django": "cart-wishes-item"}):
                item.string = '{% with total_items=wishes|length %}{% if wishes.wishes|length > 0 %}{{ total_items }}{% else %}0{% endif %}{% endwith %}'

        """ breadcrumbs """
        if soup.select('[data-django="breadcrumbs-category"]'):
            match = ['home',]
            for item in match:
                if len(self.txt_model.objects.filter(title=item, template=self.obj)) < 1:
                    text = self.txt_model(text=str.capitalize(item), title=item, template=self.obj)
                    text.save()
            for item in soup.find_all(attrs={"data-django": "breadcrumbs-category"}):
                item.string = '<span><a href="/">{{ txt_home' + '_' + str(self.obj.id) + '.text }}</a> / {% if category.parent != None %}<a href="{{ category.parent.get_absolute_url }}">{{ category.parent.title }}</a> / <a href="{{ category.get_absolute_url }}">{{ category.title }}</a>{% else %}{{ category.title }}{% endif %}</span>'

        if soup.select('[data-django="breadcrumbs-article"]'):
            match = ['home',]
            for item in match:
                if len(self.txt_model.objects.filter(title=item, template=self.obj)) < 1:
                    text = self.txt_model(text=str.capitalize(item), title=item, template=self.obj)
                    text.save()
            for item in soup.find_all(attrs={"data-django": "breadcrumbs-article"}):
                item.string = '<span><a href="/">{{ txt_home' + '_' + str(self.obj.id) + '.text }}</a> / {% if article.category != None %}<a href="{{ article.category.get_absolute_url }}">{{ article.category.title }}</a> / {% endif %}{{ article.title }}</span>'

        if soup.select('[data-django="breadcrumbs-default"]'):
            match = ['home',]
            for item in match:
                if len(self.txt_model.objects.filter(title=item, template=self.obj)) < 1:
                    text = self.txt_model(text=str.capitalize(item), title=item, template=self.obj)
                    text.save()
            for item in soup.find_all(attrs={"data-django": "breadcrumbs-default"}):
                item.string = '<span><a href="/">{{ txt_home' + '_' + str(self.obj.id) + '.text }}</a> / {{ title }}</span>'

        if soup.select('[data-django="breadcrumbs-page"]'):
            match = ['home',]
            for item in match:
                if len(self.txt_model.objects.filter(title=item, template=self.obj)) < 1:
                    text = self.txt_model(text=str.capitalize(item), title=item, template=self.obj)
                    text.save()
            for item in soup.find_all(attrs={"data-django": "breadcrumbs-page"}):
                item.string = '<span><a href="/">{{ txt_home' + '_' + str(self.obj.id) + '.text }}</a> / {{ title }}</span>'

        """ search """
        for item in soup.find_all('form', attrs={"data-django": "blog-search"}):
            item['method'] = 'get'
            item['action'] = '{% url "builder:blog_search" %}'
            if len(item.findChildren('input', attrs={"type": "text"})) > 0:
                item.findChildren('input', attrs={"type": "text"})[0]['name'] = 'search'
        for item in soup.find_all('form', attrs={"data-django": "shop-search"}):
            item['method'] = 'get'
            item['action'] = '{% url "builder:shop_search" %}'
            if len(item.findChildren('input', attrs={"type": "text"})) > 0:
                item.findChildren('input', attrs={"type": "text"})[0]['name'] = 'search'

        """ sidebar-tag """
        for item in soup.find_all(attrs={"data-django": "sidebar-tag"}):
                if item.name == 'p' or item.name == 'div':
                    parent_a = item.select_one('a')
                    parent_a['href'] = "{{ item.get_absolute_url }}"
                    parent_a.string = "{{ item.title }}"
                    for value in item.findChildren(recursive=False):
                        value.replace_with('')
                    item.append(BeautifulSoup('''{% for item in tags %}''' + str(parent_a) + '''{% endfor %}''', 'html.parser'))
                if item.name == 'ul':
                    parent_li = item.select_one('li')
                    parent_li.select_one('a')['href'] = "{{ item.get_absolute_url }}"
                    parent_li.select_one('a').string = "{{ item.title }}"
                    for value in item.findChildren(recursive=False):
                        value.replace_with('')
                    item.append(BeautifulSoup('''{% for item in tags %}''' + str(parent_li) + '''{% endfor %}''', 'html.parser'))

        """ sidebar-top-article """
        for item in soup.find_all(attrs={"data-django": "sidebar-top-article"}):
            for value in item.findChildren(recursive=False):
                value.replace_with('')
            item.name = 'div'
            item.append(BeautifulSoup('''
                        {% for item in top_post %}
                            <a href="{{ item.get_absolute_url }}">
                                <div style="display: flex; align-items:center;">
                                    <div style="width:30%;">
                                        <img alt="" src="{{ item.img.url }}" style="width: 100%; "/>
                                    </div>
                                    <div style="width:70%; padding-left:15px;">
                                        <div style="color: #000; font-size: 14px;">
                                            {{ item.created }}
                                        </div>
                                        <h6>
                                            {{ item.title }}
                                        </h6>
                                    </div>
                                </div>
                            </a>
                            <hr/>
                        {% endfor %}
                    ''', 'html.parser'))

        """ sidebar-recent-comments """
        for item in soup.find_all(attrs={"data-django": "sidebar-recent-comments"}):
            for value in item.findChildren(recursive=False):
                value.replace_with('')
            item.name = 'div'
            item.append(BeautifulSoup('''
                                {% for item in recent_comments %}
                                    <a href="{{ item.post.get_absolute_url }}">
                                        <div style="display: flex; align-items:center;">
                                            <div style="width:30%;">
                                                <img alt="" src="{{ item.post.img.url }}" style="width: 100%; "/>
                                            </div>
                                            <div style="width:70%; padding-left:15px;">
                                                <div style="color: #000; font-size: 14px;">
                                                    {{ item.created }}
                                                </div>
                                                <h6>
                                                    {{ item.body }}
                                                </h6>
                                            </div>
                                        </div>
                                    </a>
                                    <hr/>
                                {% endfor %}
                            ''', 'html.parser'))

        """ blog """
        for item in soup.find_all(attrs={"data-django": "blog"}):
            post = item.findChildren(recursive=False)[0]
            pagination = ''

            if item.select('[data-django="pagination"]'):
                pagination = soup.select_one('[data-django="pagination"]')

            if item.select('[data-django="blog-article-author"]'):
                soup.select_one('[data-django="blog-article-author"]').string = '{{ item.author.username }}'

            for value in post.findChildren(attrs={"data-django": "blog-article-tag"}):
                if value.select('i'):
                    tag_i = value.select_one('i')
                    for children in value.findChildren():
                        children.replace_with('')
                    value.string = ''
                    value.append(tag_i)
                    value.append(
                        '{% for tag in item.tags.all %} <a href="{{ tag.get_absolute_url }}" style="display:inline;">{{ tag.title }}</a> {% endfor %}')
                else:
                    value.string = '{% for tag in item.tags.all %} <a href="{{ tag.get_absolute_url }}" style="display:inline;">{{ tag.title }}</a> {% endfor %}'

            for value in item.findChildren(recursive=False):
                value.replace_with('')
            for value in post.findChildren('img'):
                value['src'] = '{{ item.img.url }}'
                value.replace_with(
                    BeautifulSoup('''{% if item.img is not None %}''' + str(value) + '''{% endif %}''', 'html.parser'))
            for value in post.findChildren('a'):
                if value.has_attr('data-django-link'):
                    pass
                else:
                    if '{{' in value['href']:
                        pass
                    else:
                        value['href'] = '{{ item.get_absolute_url }}'


            for value in post.findChildren(attrs={"data-django": "blog-article-date"}):
                if value.select('i'):
                    tag_i = value.select_one('i')
                    for children in value.findChildren():
                        children.replace_with('')
                    value.string = ''
                    value.append(tag_i)
                    value.append('{{ item.created }}')
                else:
                    value.string = '{{ item.created }}'

            for value in post.findChildren(attrs={"data-django": "blog-article-comment"}):
                if value.select('i'):
                    tag_i = value.select_one('i')
                    for children in value.findChildren():
                        children.replace_with('')
                    value.string = ''
                    value.append(tag_i)
                    value.append('{{ item.comment_set.count }}')  # '{% with comments.count as total_comments %}{% if total_comments > 0 %}{{ total_comments }}{% else %}0{% endif %}{% endwith %}'
                else:
                    value.string = '{{ item.comment_set.count }}'  # '{% with comments.count as total_comments %}{{ total_comments }}{% endwith %}'
            for value in post.findChildren(attrs={"data-django": "blog-article-title"}):
                value.string = '<a href="{{ item.get_absolute_url }}">{{ item.title }}</a>'
            for value in post.findChildren(attrs={"data-django": "blog-article-intro"}):
                value.string = '{{ item.intro }}'
            item.append(BeautifulSoup('''{% for item in posts %}''' + str(post) + '''{% endfor %}''' + str(pagination),
                                      'html.parser'))

        """ article """
        for value in soup.find_all(attrs={"data-django": "article-body"}):
            value.string = '{{ article.body | safe}}'
        for value in soup.find_all(attrs={"data-django": "article-title"}):
            value.string = '{{ article.title }}'
        for value in soup.find_all(attrs={"data-django": "article-img"}):
            value['src'] = '{{ article.img.url }}'
        for value in soup.find_all(attrs={"data-django": "article-author"}):
            value.string = '{{ article.author.username }}'
        for value in soup.find_all(attrs={"data-django": "article-date"}):
            if value.select('i'):
                tag_i = value.select_one('i')
                for children in value.findChildren():
                    children.replace_with('')
                value.string = ''
                value.append(tag_i)
                value.append('{{ article.created }}')
            else:
                value.string = '{{ article.created }}'
        for value in soup.find_all(attrs={"data-django": "article-comment"}):
            if value.select('i'):
                tag_i = value.select_one('i')
                for children in value.findChildren():
                    children.replace_with('')
                value.string = ''
                value.append(tag_i)
                value.append(
                    '{{ article.comment_set.count }}')
            else:
                value.string = '{{ article.comment_set.count }}'
        for value in soup.find_all(attrs={"data-django": "article-tag"}):
            if value.select('i'):
                tag_i = value.select_one('i')
                for children in value.findChildren():
                    children.replace_with('')
                value.string = ''
                value.append(tag_i)
                value.append(
                    '{% for tag in article.tags.all %} <a href="{{ tag.get_absolute_url }}" style="display:inline;">{{ tag.title }}</a> {% endfor %}')
            else:
                value.string = '{% for tag in article.tags.all %} <a href="{{ tag.get_absolute_url }}" style="display:inline;">{{ tag.title }}</a> {% endfor %}'

        """ pagination """
        for item in soup.find_all(attrs={"data-django": "pagination"}):
            for value in item.findChildren(recursive=False):
                value.replace_with('')
            item.string = ''
            item.append(BeautifulSoup("""
                        {% if is_paginated %}
                        <ul class="pagination">
                            {% if page_obj.has_previous %}
                                <li><a href="?page={{ page_obj.previous_page_number }}">&laquo;</a></li>
                            {% else %}
                                <li class="disabled"><a href="javascript:void(0);"><span>&laquo;</span></a></li>
                            {% endif %}
                            {% for i in paginator.page_range %}
                                {% if page_obj.number == i %}
                                    <li class="active"><a href="javascript:void(0);"><span>{{ i }} <span class="sr-only">(current)</span></span></a></li>
                                {% else %}
                                    <li><a href="?page={{ i }}">{{ i }}</a></li>
                                {% endif %}
                            {% endfor %}
                            {% if page_obj.has_next %}
                                <li><a href="?page={{ page_obj.next_page_number }}">&raquo;</a></li>
                            {% else %}
                                <li class="disabled"><a href="javascript:void(0);"><span>&raquo;</span></a></li>
                            {% endif %}
                        </ul>
                    {% endif %}
                    """, 'html.parser'))

        """ form-subscribe """
        for item in soup.find_all('form', attrs={"data-django": "form-subscribe"}):
            item['method'] = 'post'
            item['action'] = "{% url 'account:subscribe' %}"
            input_subscribe = item.select_one('input')
            input_subscribe['name'] = 'email'
            input_subscribe['type'] = 'email'
            slug = hashlib.md5('Enter your mail'.encode("utf-8")).hexdigest()
            if len(self.txt_model.objects.filter(title=slug, template=self.obj)) < 1:
                text = self.txt_model(text='Enter your mail', title=slug, template=self.obj)
                text.save()
            input_subscribe['placeholder'] = '{{ txt_' + slug + '.text }}'
            button_subscribe = item.select_one('button')
            button_subscribe['type'] = 'submit'
            tag_i = ''
            if item.select('i'):
                tag_i = item.select_one('i')
            children = item.findChildren(recursive=False)
            for child in children:
                child.replace_with('')
            item.append('{% csrf_token %}')
            item.append(input_subscribe)
            item.append(tag_i)
            item.append(button_subscribe)

        """ form-message """
        for item in soup.find_all('form', attrs={"data-django": "form-message"}):
            item['method'] = 'post'
            item['action'] = "{% url 'account:message' %}"
            item.append('{% csrf_token %}')

        """ form-comments """
        for value in soup.find_all(attrs={"data-django": "form-comments-title"}):
            value.string = '{{ total_comments }} comment{{ total_comments|pluralize }}'
            value.replace_with(BeautifulSoup('''{% with comments.count as total_comments %}''' + str(value) + '''{% endwith %}''', 'html.parser'))

        for item in soup.find_all(attrs={"data-django": "form-comments"}):
            first_tag_list = item.findChildren(recursive=False)[0]

            for value in item.findChildren(recursive=False):
                value.replace_with('')

            for value in first_tag_list.findChildren(attrs={"data-django": "form-comments-photo"}):
                value['src'] = "{% static '/admin/img/user.png' %}"
                value['style'] = "width:100px;height:100px;"

            for value in first_tag_list.findChildren(attrs={"data-django": "form-comments-author"}):
                if value.select('i'):
                    tag_i = value.select_one('i')
                    for children in value.findChildren():
                        children.replace_with('')
                    value.string = ''
                    value.append(tag_i)
                    value.append('{{ comment.name }}')
                else:
                    value.string = '{{ comment.name }}'

            for value in first_tag_list.findChildren(attrs={"data-django": "form-comments-body"}):
                value.string = '{{ comment.body | linebreaks }}'

            for value in first_tag_list.findChildren(attrs={"data-django": "form-comments-date"}):
                if value.select('i'):
                    tag_i = value.select_one('i')
                    for children in value.findChildren():
                        children.replace_with('')
                    value.string = ''
                    value.append(tag_i)
                    value.append('{{ comment.created }}')
                else:
                    value.string = '{{ comment.created }}'

            for value in first_tag_list.findChildren(attrs={"data-django": "form-comments-reply"}):
                pass

            item.append(BeautifulSoup('''
                                        {% for comment in comments %}''' + str(first_tag_list) + '''
                                        {% empty %}
                                            <p>There are no comments yet.</p>
                                        {% endfor %}
                                        {% if new_comment %}
                                            <h2>Your comment has been added.</h2>
                                        {% else %}
                                            <h2>Add a new comment</h2>
                                            <form action="." method="post">
                                                {{ comment_form.as_p }}
                                                {% csrf_token %}
                                                <p><input type="submit" value="Add comment"></p>
                                            </form>
                                        {% endif %}''', 'html.parser'))

        """ html """
        for item in soup.find_all(attrs={"data-django": "html"}):
            html_string = ''
            children = item.findChildren(recursive=False)
            for child in children:
                html_string += str(child)
                child.replace_with('')

            slug = hashlib.md5(html_string.encode("utf-8")).hexdigest()
            item.string = '{{ html_' + str(slug) + '_' + str(self.obj.id) + '.html | safe }}'

            if len(self.html_model.objects.filter(title=str(slug), template=self.obj)) < 1:
                text = self.html_model(html=html_string, title=str(slug), template=self.obj)
                text.save()

        """ text """
        for item in soup.strings:
            str_item = re.sub(" +", " ", item)
            str_item = str_item.replace('\n', '').replace('\r', '')
            if "{{" in str_item or "{%" in str_item or len(str_item) < 2:
                pass
            else:
                slug = hashlib.md5(str_item.encode("utf-8")).hexdigest()
                soup = BeautifulSoup(str(soup).replace(item, '{{ txt_' + str(slug) + '_' + str(self.obj.id) + '.text }}'), 'html.parser')
                if len(self.txt_model.objects.filter(title=str(slug), template=self.obj)) < 1:
                    text = self.txt_model(text=str_item, title=str(slug), template=self.obj)
                    text.save()

        with open(os.path.join(settings.BASE_DIR, 'templates/' + str(self.obj.slug)), 'w', encoding="utf-8") as f:
            if soup.select('html'):
                f.write(
                    '{% load static %} {% load compress %} {% load mptt_tags %} {% load i18n %} <!DOCTYPE html>' + str(
                        soup.html.prettify(formatter=None)))
            else:
                f.write('{% load static %} {% load compress %} {% load mptt_tags %} {% load i18n %}' + str(
                    soup.prettify(formatter=None)))

    def template_static(self):
        list_default_template = os.listdir(os.path.join(settings.BASE_DIR, 'static/template_static/'))
        for html in list_default_template:
            soup = BeautifulSoup(
                open(os.path.join(settings.BASE_DIR, 'static/template_static/' + html), encoding='utf-8'),
                'html.parser')
            ''' text '''
            for text in soup.find_all(attrs={"data-django": "text-default"}):
                for item in text:
                    str_item = re.sub(" +", " ", item)
                    str_item = str_item.replace('\n', '').replace('\r', '')
                    if "{{" in str_item or "{%" in str_item or len(str_item) < 2:
                        pass
                    else:
                        slug = hashlib.md5(str_item.encode("utf-8")).hexdigest()
                        soup = BeautifulSoup(str(soup).replace(item, '{{ txt_' + str(slug) + '_' + str(self.obj.id) + '.text }}'), 'html.parser')
                        if len(Text.objects.filter(title=str(slug), template=self.obj)) < 1:
                            new_text = Text(text=item, title=str(slug), template=self.obj)
                            new_text.save()
            ''' html '''
            for item in soup.find_all(attrs={"data-django": "html-default"}):
                html_string = ''
                children = item.findChildren(recursive=False)
                for child in children:
                    html_string += str(child)
                    child.replace_with('')

                slug = hashlib.md5(html_string.encode("utf-8")).hexdigest()
                item.string = '{{ html_' + str(slug) + '_' + str(self.obj.id) + '.html | safe }}'

                if len(self.html_model.objects.filter(title=str(slug), template=self.obj)) < 1:
                    text = self.html_model(html=html_string, title=str(slug), template=self.obj)
                    text.save()

            with open(os.path.join(settings.BASE_DIR, 'templates/default_' + html), 'w', encoding="utf-8") as f:
                f.write(str(soup.prettify(formatter=None)))
