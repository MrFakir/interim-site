from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q

from django.views.generic import CreateView

from posts.models import Post
from .models import *
from django.urls import reverse_lazy

from django.core.mail import send_mail
from .forms import ContactForm


class SendContacts(SuccessMessageMixin, CreateView):
    model = Clients
    success_url = reverse_lazy('send-contacts')
    form_class = ContactForm
    template_name = 'send_contact/clients_form.html'
    success_message = 'Спасибо, мы с Вами свяжемся в ближайшее или указанное Вами время.'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promo_category'] = Post.objects.filter(
            Q(category__title__icontains='ООО') | Q(category__title__icontains='ИП')).order_by('-pk')
        return context
