from django import template
from main_page.models import MainPageModel

register = template.Library()


@register.inclusion_tag('main_page/get_start_block.html')
def show_get_start_block():
    try:
        context = MainPageModel.objects.filter(title__icontains='block_for_special_item5').first()
        return {'get_start_block': context.json_field}
    except AttributeError:
        return {'get_start_block': 'context.json_field'}
