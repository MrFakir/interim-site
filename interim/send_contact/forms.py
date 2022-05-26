from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from .models import Clients
from captcha.fields import CaptchaField


class ContactForm(forms.ModelForm):
    captcha = CaptchaField(help_text='Введите символы с картинки')

    class Meta:
        model = Clients
        fields = ['name', 'company', 'email', 'phone', 'message', 'captcha']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={
                'placeholder': 'Введите свой комментарий, например в какие часы с Вами связаться.',
                'class': 'form-control',
                'rows': 10,
            }),
        }
