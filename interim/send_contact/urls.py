from django.urls import path

from .views import *

urlpatterns = [
    path('send-contacts/', SendContacts.as_view(), name='send-contacts'),
]
