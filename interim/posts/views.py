from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import *


# @cache_page(15)



class CategoryList(ListView):
    template_name = 'posts/category.html'
    context_object_name = 'category'

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class SinglePost(DetailView):
    model = Post
    template_name = 'posts/single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promo_category'] = Post.objects.filter(
            Q(category__title__icontains='ООО') | Q(category__title__icontains='ИП')).order_by('-pk')
        return context
