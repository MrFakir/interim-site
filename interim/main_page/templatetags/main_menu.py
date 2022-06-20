from django import template
from posts.models import Category
from django.db import models

register = template.Library()


@register.inclusion_tag('main_page/menu_tpl.html')
def show_main_menu(menu_class=''):
    categories = Category.objects.all().order_by('order')[:5]
    return {'categories': categories, 'menu_class': menu_class}
