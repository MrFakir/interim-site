from django.urls import path

from .views import *


urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('category/<str:slug>/', CategoryList.as_view(), name='category'),
    path('<str:category>/<str:slug>/', SinglePost.as_view(), name='single'),
    # path('testapi/', MyAPIView.as_view(), name='testapi'),
]
