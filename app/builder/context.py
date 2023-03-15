from .models import Category, Menu, Image, Link, Text, Html


def get_context():
    context = {}
    for item in Menu.objects.filter(parent=None):
        context['menu_' + item.slug] = Menu.objects.get(slug=item.slug, parent=None).get_descendants()
    for item in Category.objects.filter(parent=None):
        context['category_' + item.slug] = Category.objects.get(slug=item.slug, parent=None).get_descendants()
    img_template_all = Image.objects.all()
    for item in img_template_all:
        context['img_' + item.title + '_' + str(item.template.id)] = item
    link_template_all = Link.objects.all()
    for item in link_template_all:
        context['link_' + item.title + '_' + str(item.template.id)] = item
    text_template_all = Text.objects.all()
    for item in text_template_all:
        context['txt_' + str(item.title) + '_' + str(item.template.id)] = item
    html_template_all = Html.objects.all()
    for item in html_template_all:
        context['html_' + str(item.title) + '_' + str(item.template.id)] = item
    return context
