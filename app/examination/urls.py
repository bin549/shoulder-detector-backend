from django.urls import path
from . import views

app_name = 'examination'

urlpatterns = [
    path('savefile/', views.savefile, name='savefile'),
    path('get/', views.ExaminationAPI.as_view()),
    path('list/', views.ExaminationAPI.as_view()),
]
