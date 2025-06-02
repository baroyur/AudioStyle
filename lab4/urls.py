from django.urls import path
from . import views

app_name = 'lab4'

urlpatterns = [
    path('report/', views.report, name='report'),
]
