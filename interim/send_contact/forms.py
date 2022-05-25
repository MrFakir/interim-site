from django import forms
from .models import Clients


class ContactForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['name', 'company', 'email', 'phone', 'message']
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
