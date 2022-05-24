from django.forms import ModelForm, Textarea
from .models import Clients


class ContactForm(ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'
        widgets = {'message': Textarea(
            attrs={
                'placeholder': 'Введите свой комментарий, например в какие часы с Вами связаться.'
            }
        )}
