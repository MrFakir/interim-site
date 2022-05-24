from django.urls import path

from .views import *

urlpatterns = [
    path('send-contacts', SendContacts.as_view(), name='send-contacts'),
    path('send-contacts-ok', SendOk.as_view(), name='send-ok'),
]
