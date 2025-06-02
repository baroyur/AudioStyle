from django.urls import path
from . import views

app_name = 'lab6'

urlpatterns = [
    path('', views.start_test, name='start'),
    path('test/<int:student_id>/<int:question_number>/', views.question_view, name='question'),
    path('results/<int:student_id>/', views.result_view, name='results'),
]
