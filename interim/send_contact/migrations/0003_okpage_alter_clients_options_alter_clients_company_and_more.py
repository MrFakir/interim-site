# Generated by Django 4.0.3 on 2022-05-24 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('send_contact', '0002_rename_contact_clients'),
    ]

    operations = [
        migrations.CreateModel(
            name='OkPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок страницы')),
                ('content', models.TextField(max_length=1000, verbose_name='Контент')),
                ('post_img', models.ImageField(blank=True, upload_to='post_img/%Y/%m/%d/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Страница благодарности за связь',
                'verbose_name_plural': 'Страницы благодарности за связь',
                'ordering': ['-pk'],
            },
        ),
        migrations.AlterModelOptions(
            name='clients',
            options={'ordering': ['-pk'], 'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterField(
            model_name='clients',
            name='company',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='message',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Полное имя'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='phone',
            field=models.CharField(max_length=12, verbose_name='Телефон'),
        ),
    ]
