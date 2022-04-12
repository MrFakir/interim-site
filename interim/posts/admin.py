import re

from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from interim.settings import JSON_DATA_SCHEMA
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .json_view import JsonForm, JsonView


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


class MainPageModelAdmin(JsonView):

    save_on_top = True
    list_display = ['title', 'get_json_title', 'get_json_image']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MainPageModel, MainPageModelAdmin)
