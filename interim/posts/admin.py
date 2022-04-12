import datetime
import re

from django.contrib import admin
from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe

from interim.settings import JSON_DATA_SCHEMA, MEDIA_URL
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .json_view import JsonForm


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    save_on_top = True
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True


class MainPageModelAdminForm(JsonForm):

    class Meta:
        model = MainPageModel
        exclude = ['json_field', ]


class MainPageModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        return MainPageModelAdminForm

    def get_fieldsets(self, request, obj=None):
        # получаем список полей для отображения, без этого хоть убей не видит наши кастомные поля, хотя они создаются
        fieldsets = super(MainPageModelAdmin, self).get_fieldsets(request, obj)
        for i in JSON_DATA_SCHEMA.keys():
            fieldsets[0][1]['fields'] += [i]
        return fieldsets

    @staticmethod
    def pars_json(obj, local_json_field=''):  # метод, которым мы парсим json, для отображения в админке
        if obj.json_field: # если объект в принципе есть (не новая запись)
            json_obj = obj.json_field
            if local_json_field in json_obj.keys():  # смотрим, есть ли текущий ключ в файле
                if re.search(r'image*', local_json_field):  # способ отдельного вывода для изображений
                    return mark_safe(f'<img src="{json_obj[local_json_field]}" width="100">')
                elif re.search(r'text*', local_json_field):  # а эт для текста вывод
                    return json_obj[local_json_field]
        else:
            return mark_safe('<p>Объект пуст</p>')  # ну и вывод для пустого объекта

    def get_json_image(self, obj):
        return self.pars_json(obj, local_json_field='image')

    def get_json_title(self, obj):
        return self.pars_json(obj, local_json_field='text')

    get_json_image.short_description = 'Миниатюра'
    get_json_title.short_description = 'Текст'
    save_on_top = True
    list_display = ['title', 'get_json_title', 'get_json_image']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MainPageModel, MainPageModelAdmin)
