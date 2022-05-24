import datetime

from django.db.models import Q
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.views.generic import CreateView

from posts.models import Post
from .models import *
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import ContactForm


class SendContacts(CreateView):
    model = Clients
    success_url = reverse_lazy('send-ok')
    form_class = ContactForm

    def form_valid(self, form):
        data = form.data
        send_mail(
            subject=f'Сообщение с Interim, с формы обратной связи',
            message=f'Имя: {data["name"]};\nКомпания: {data["company"]};\nТелефон: {data["phone"]};\n'
                    f'Почта: {data["email"]};\nСообщение: {data["email"]}.',
            from_email='fakir_x@mail.ru',
            recipient_list=['fakir_x@mail.ru', ]
        )
        return super().form_valid(form)


class SendOk(DetailView):
    model = OkPage
    template_name = 'send_contact/thanks_page.html'
    context_object_name = 'ok_page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promo_category'] = Post.objects.filter(
            Q(category__title__icontains='ООО') | Q(category__title__icontains='ИП')).order_by('-pk')
        return context
