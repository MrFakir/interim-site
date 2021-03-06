from datetime import date
from re import search

from django import forms
from django.contrib import admin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe

from interim.settings import JSON_DATA_SCHEMA, MEDIA_URL
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class JsonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # наследуем все что было в init
        if not self.instance.json_field:  # если наш json файл(поле) в словаре пустой
            # Новый объект
            for i in JSON_DATA_SCHEMA.keys():  # создаем поля на основе константы в settings
                if search(r'image*', i):  # выбираем только поля начинающиеся на image
                    self.fields[i] = forms.ImageField(required=False, help_text='Поле для изображения')
                elif search(r'text*', i):  # выбираем только поля начинающиеся на text
                    self.fields[i] = forms.CharField(max_length=255, required=False, help_text='Поле для текста')
                elif search(r'content*', i):  # выбираем только поля начинающиеся на content
                    self.fields[i] = forms.CharField(required=False, help_text='Поле для большого текста',
                                                     widget=CKEditorUploadingWidget())
                elif search(r'url*', i):  # выбираем только поля начинающиеся на url
                    self.fields[i] = forms.CharField(max_length=255, required=False, help_text='Поле для ссылки')
        else:
            # Старый объект
            json_for_filling = self.instance.json_field  # так как это старый объект, забираем всё что было в нашем json
            for i in JSON_DATA_SCHEMA.keys():  # пробегаемся по нашей константе, для заполнения полей
                if search(r'image*', i):  # выбираем поля image
                    if i in json_for_filling.keys():  # проверяем есть ли текущий ключ константы, в json из базы
                        self.fields[i] = forms.ImageField(required=False, help_text=mark_safe(f"""
                            <b>Текущее изображение</b></br><img src="{json_for_filling[i]}" 
                            width="300" ></br>При замене изображения,
                            оно поменяется тут только ПОСЛЕ обновления страницы"""))
                    else:  # отображаем другой лейбл с картинкой, решение конечно не ахти, но ничего другого не придумал
                        self.fields[i] = forms.ImageField(required=False, help_text='Поле для изображения')
                elif search(r'text*', i):  # выбираем поле text
                    if i in json_for_filling.keys():  # проверяем есть ли текущий ключ константы, в json из базы
                        self.fields[i] = forms.CharField(max_length=255, required=False, help_text='Поле для текста',
                                                         initial=json_for_filling[i])  # заполняем поле старым значением
                    else:
                        self.fields[i] = forms.CharField(max_length=255, required=False, help_text='Поле для текста')
                elif search(r'content*', i):  # выбираем поле text
                    if i in json_for_filling.keys():  # проверяем есть ли текущий ключ константы, в json из базы
                        self.fields[i] = forms.CharField(required=False,
                                                         help_text='Поле для большого текста',
                                                         initial=json_for_filling[i],  # заполняем поле старым значением
                                                         widget=CKEditorUploadingWidget())
                    else:
                        self.fields[i] = forms.CharField(required=False,
                                                         help_text='Поле для большого текста',
                                                         widget=CKEditorUploadingWidget())
                elif search(r'url*', i):  # выбираем поле url
                    if i in json_for_filling.keys():  # проверяем есть ли текущий ключ константы, в json из базы
                        self.fields[i] = forms.CharField(max_length=255, required=False, help_text='Поле для ссылки',
                                                         initial=json_for_filling[i])  # заполняем поле старым значением
                    else:
                        self.fields[i] = forms.CharField(max_length=255, required=False, help_text='Поле для ссылки')

    def save(self, commit=True):
        instance = super(JsonForm, self).save(commit=False)
        json_dir = {}

        def save_image(image):
            # функция сохранения изображения
            date_path = date.today().strftime('%Y/%m/%d')
            return default_storage.save(f'front_page_img/{date_path}/{str(image)}', ContentFile(image.read()))

        # заполнение полей на основе полученных данных
        for i in self.fields:  # прогоняем все поля
            if i not in self.base_fields:  # если поля кастомные (не содержаться в списке base_fields
                if self.cleaned_data.get(i, None):  # если поле не пустое
                    if not search(r'image*', i):  # если поле не картинка, для картинок отдельный метод
                        json_dir[i] = self.cleaned_data.get(i, None)  # пишем значение поля в словарь
                    else:
                        json_dir[i] = MEDIA_URL + save_image(self.cleaned_data.get(i, None))  # сохраняем изображение
                        # и пишем ссылку на него в словарь

        if json_dir:  # если вообще что нибудь поменяли
            instance.json_field.update(json_dir)  # расширяем словарь новыми (изменёнными) значениями, не трогая старые
        if commit:
            instance.save()  # save :)
        return instance


class JsonView(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        return JsonForm

    def get_fieldsets(self, request, obj=None):
        # получаем список полей для отображения, без этого хоть убей не видит наши кастомные поля, хотя они создаются
        fieldsets = super(JsonView, self).get_fieldsets(request, obj)
        for i in JSON_DATA_SCHEMA.keys():
            fieldsets[0][1]['fields'] += [i]
        return fieldsets

    @staticmethod
    def pars_json(obj, local_json_field=''):  # метод, которым мы парсим json, для отображения в админке
        if obj.json_field:  # если объект в принципе есть (не новая запись)
            json_obj = obj.json_field
            if local_json_field in json_obj.keys():  # смотрим, есть ли текущий ключ в файле
                if search(r'image*', local_json_field):  # способ отдельного вывода для изображений
                    return mark_safe(f'<img src="{json_obj[local_json_field]}" width="100">')
                elif search(r'text*', local_json_field):  # а эт для текста вывод
                    return json_obj[local_json_field]
        else:
            return mark_safe('<p>Объект пуст</p>')  # ну и вывод для пустого объекта

    def get_json_image(self, obj):
        return self.pars_json(obj, local_json_field='image')

    def get_json_title(self, obj):
        return self.pars_json(obj, local_json_field='text')

    get_json_image.short_description = 'Миниатюра'
    get_json_title.short_description = 'Текст'
