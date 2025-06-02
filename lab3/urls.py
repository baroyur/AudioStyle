from django.urls import path
from . import views

app_name = 'lab3'

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('add-car/', views.add_car, name='add_car'),
    path('add-parameter/', views.add_car_parameter, name='add_car_parameter'),
    path('add-manufacturer/', views.add_manufacturer, name='add_manufacturer'),
    path('add-car-class/', views.add_car_class, name='add_car_class'),
]
