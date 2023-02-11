from django import template
from ..models import Article, Comment
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def comments_count(article_id):
    return Comment.objects.filter(post_id=article_id).count()


@register.inclusion_tag('blog/latest_post_comments.html')
def show_latest_comments(article_id, count=5):
    latest_comments = Comment.objects.filter(post_id=article_id).order_by('-created')[:count]
    return {'latest_comments': latest_comments}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

# @register.assignment_tag
# def get_most_commented_posts(count=5):
#     return Posts.is_published.annotate(comments_count=comments_count('post_id')).order_by('-total_comments')[:count]


# simple_tag: str
# inclusion_tag: arr template
# assignment_tag: value

