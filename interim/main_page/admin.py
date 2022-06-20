from django.contrib import admin
from .json_view import JsonForm, JsonView
from .models import MainPageModel


class MainPageModelAdminForm(JsonForm):
    class Meta:
        model = MainPageModel
        exclude = ['json_field', ]


class MainPageModelAdmin(JsonView):
    def get_form(self, request, obj=None, change=False, **kwargs):
        return MainPageModelAdminForm

    save_on_top = True
    save_as = True
    list_display = ['title', 'get_json_title', 'get_json_image']


admin.site.register(MainPageModel, MainPageModelAdmin)
