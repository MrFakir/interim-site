from django.db import models

from interim.settings import MAIN_PAGE_BLOCKS


class MainPageModel(models.Model):
    title = models.CharField(max_length=500, choices=MAIN_PAGE_BLOCKS, verbose_name='Название блока на главной страницы',
                             help_text='''Название должно быть на латинице, будет использоваться
                             в качестве переменной для Views''')
    json_field = models.JSONField(null=False, default=dict,
                                  blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Объект главной страницы'
        verbose_name_plural = 'Отображение главной страницы'
