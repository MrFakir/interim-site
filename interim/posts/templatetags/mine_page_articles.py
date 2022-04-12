from django import template
from posts.models import Post
from django.db import models
from django.db.models import Q

register = template.Library()


@register.inclusion_tag('posts/main_page_articles_tpl.html')
def show_main_page_articles():
    data_cat = Post.objects.filter(Q(category__title__icontains='ООО') | Q(category__title__icontains='ИП'))
    first_category = data_cat.filter(category__title__icontains='ООО')[:3]
    second_category = data_cat.filter(category__title__icontains='ИП')[:3]
    try:
        url_first_category = first_category.first().category.get_absolute_url()
        url_second_category = second_category.first().category.get_absolute_url()

        return {'first_category': first_category, 'second_category': second_category,
                'url_first_category': url_first_category, 'url_second_category': url_second_category}
    except AttributeError:
        return {'first_category': first_category, 'second_category': second_category,
                'url_first_category': 'url_first_category', 'url_second_category': 'url_second_category'}

