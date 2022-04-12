from django import forms
from django.forms import MultiWidget


class CustomJSONofDOC(forms.Widget):
    pass


class SuperTestWidget(MultiWidget):

    value = 123

    def decompress(self, value):
        if value:
            return [value.date(), value.time()]
        return [None, None]
