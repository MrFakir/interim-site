from django.db import models


class Clients(models.Model):
    name = models.CharField(max_length=250, verbose_name='Полное имя')
    company = models.CharField(max_length=250, null=True, blank=True, verbose_name='Компания')
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    message = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
