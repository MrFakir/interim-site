from django import forms
from .models import *


# class MainPageModelForm(forms.ModelForm):
#     class Meta:
#         model = MainPageModel
#         exclude = []
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for x in ['e1', 'e2', 'e3']:
#             self.base_fields[x] = forms.CharField()
#             self.fields[x] = forms.CharField()



