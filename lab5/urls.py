from django.urls import path
from . import views

app_name = 'lab5'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:poll_id>/', views.poll_view, name='poll'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),
]
