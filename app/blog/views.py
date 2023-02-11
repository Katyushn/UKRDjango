from django.shortcuts import render, get_object_or_404
from .models import Article, Comment
from django.views.generic import ListView, DetailView
from .forms import ArticleShareEmailForm, CommentForm
from django.core.mail import send_mail
from django.shortcuts import redirect
from builder.models import Template, Menu, Image, Link, Text, Html, Category, Tag
from builder.context import get_context


class BlogCategory(ListView):
    paginate_by = 5
    model = Article
    context_object_name = 'posts'
    allow_empty = True

    def get_template_names(self, *, object_list=None, **kwargs):
        if 'blog_category_slug' in self.kwargs:
            category = Category.objects.get(slug=self.kwargs['blog_category_slug'], pk=self.kwargs['blog_category_id'])
            if category.template:
                return category.template.slug
            else:
                return Template.objects.get(type='blog', default=True).slug
        else:
            return Template.objects.get(type='blog', default=True).slug

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        add_context = get_context()
        context.update(add_context)
        if 'blog_category_slug' in self.kwargs:
            context['category'] = Category.objects.get(slug=self.kwargs['blog_category_slug'], pk=self.kwargs['blog_category_id'])
            context['title'] = context['category'].title
        context['top_post'] = Article.objects.filter(status='top', category__isnull=False,).order_by('updated')[:5]
        context['recent_comments'] = Comment.objects.filter(active=True).order_by('updated')[:5]
        if 'category' in context:
            context['tags'] = Tag.objects.filter(id__in=context['category'].tags.all())
        return context

    list_all_category = []

    def category_recursive(self):
        for value in self.list_all_category:
            for item in Category.objects.filter(parent=value):
                if item.id not in self.list_all_category:
                    self.list_all_category.append(item.id)
                    self.category_recursive()

    def get_queryset(self):
        self.list_all_category = [self.kwargs['blog_category_id']]
        self.category_recursive()
        return Article.objects.filter(category__in=self.list_all_category).select_related('category')


class BlogTag(BlogCategory):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['item_slug'], pk=self.kwargs['item_id'])
        context['title'] = context['tag'].title
        return context

    def get_queryset(self):
        return Article.objects.filter(tags=self.kwargs['item_id'])


class BlogSearch(BlogCategory):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search'
        return context

    def get_queryset(self):
        return Article.objects.filter(title__contains=self.request.GET.get('search'))


class BlogArticle(DetailView):
    model = Article
    context_object_name = 'article'
    pk_url_kwarg = 'post_id'

    def get_template_names(self, *, object_list=None, **kwargs):
        if 'post_slug' in self.kwargs:
            article = Article.objects.get(slug=self.kwargs['post_slug'], pk=self.kwargs['post_id'])
            if article.template:
                return article.template.slug
            else:
                return Template.objects.get(type='article', default=True).slug
        else:
            return Template.objects.get(type='article', default=True).slug

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        template_context = get_context()
        context.update(template_context)
        get_object_or_404(Article.objects.filter(
            category__slug=self.kwargs['blog_category_slug'],
            category_id=self.kwargs['blog_category_id'],
            slug=self.kwargs['post_slug'],
            id=self.kwargs['post_id']))
        context['comments'] = Comment.objects.filter(post=context['article'].id, active=True)
        context['title'] = context['article'].title
        context['tags'] = Tag.objects.all()
        context['comment_form'] = CommentForm(initial={'post': self.object})
        context['top_post'] = Article.objects.filter(status='top', category__isnull=False,).order_by('updated')[:5]
        context['recent_comments'] = Comment.objects.filter(active=True).order_by('updated')[:5]
        for item in Menu.objects.filter(parent=None):
            context['menu_' + item.slug] = Menu.objects.get(slug=item.slug, parent=None).get_descendants(
                include_self=False)
        for item in Category.objects.filter(parent=None):
            context['category_' + item.slug] = Category.objects.get(slug=item.slug, parent=None).get_descendants()
        context['tags'] = Tag.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            post = get_object_or_404(Article.objects.filter(
                category__slug=self.kwargs['blog_category_slug'],
                category_id=self.kwargs['blog_category_id'],
                slug=self.kwargs['post_slug'],
                id=self.kwargs['post_id']))
            # Create Comment object but don't save to database yet
            new_comment = form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return redirect(post.get_absolute_url())
        else:
            self.object = self.get_object()
            context = super().get_context_data(**kwargs)
            context['comment_form'] = CommentForm
            return self.render_to_response(context=context)


def error404(request, exception):
    if len(Template.objects.filter(type='404', default=True)) < 1:
        template = Template.objects.get(type='default', default=True).slug
    else:
        template = Template.objects.get(type='404', default=True).slug
    context = get_context()
    context['main'] = 'default_404.html'
    context['title'] = '404'
    print(context)
    response = render(request, template, context)
    response.status_code = 404
    return response


def article_share_email(request, *args, **kwargs):
    template = Template.objects.get(type='default', default=True).slug
    context = get_context()
    context['main'] = 'default_share.html'
    context['title'] = ''
    context['post'] = get_object_or_404(Article, id=kwargs['value_id'], is_published=True)
    context['sent'] = False
    if request.method == 'POST':
        context['form'] = ArticleShareEmailForm(request.POST)
        if context['form'].is_valid():
            cd = context['form'].cleaned_data
            post_url = request.build_absolute_uri(context['post'].get_absolute_url())
            subject = '{} ({}) recommends you to read the article "{}"'.format(cd['name'], cd['email_from'], context['post'].title)
            message = 'Check out the article: "{}" by the address {}\n\n Commentary on the article from {}: {}'.format(context['post'].title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'katyushn@gmail.com', [cd['email_to']])
            context['sent'] = True
    else:
        context['form'] = ArticleShareEmailForm()
    return render(request, template, context)
