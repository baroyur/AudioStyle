from django.urls import path
from . import views

app_name = 'labs'

urlpatterns = [
    path('', views.index, name='index'),  # labs/
    path('lab1/', views.lab1, name='lab1'),
    path('lab2/', views.lab2_form, name='lab2_form'),
]
