from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from interim.settings import MAIN_PAGE_BLOCKS


# Основной контент
class Category(models.Model):
    title = models.CharField(max_length=10, verbose_name='Название категории')
    slug = models.SlugField(max_length=10, verbose_name='url(ссылка)', unique=True)
    order = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)],
                                             verbose_name='Порядок вывода')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=50, verbose_name='url(ссылка)', unique=True)
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    post_img = models.ImageField(upload_to='post_img/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single', kwargs={'category': self.category.slug, 'slug': self.slug})

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


# Контент главной страницы


