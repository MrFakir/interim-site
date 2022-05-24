from django.db import models


class Clients(models.Model):
    name = models.CharField(max_length=250)
    company = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=12)
    message = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.email

