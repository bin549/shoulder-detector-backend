from django.urls import path
from . import views

app_name = 'examination'

urlpatterns = [
    path('upload/', views.savefile, name='savefile'),
    path('get/', views.ExaminationAPI.as_view()),
    path('list/', views.ExaminationAPI.as_view()),
    path('type/list/', views.ExaminationTypeAPI.as_view()),
]
