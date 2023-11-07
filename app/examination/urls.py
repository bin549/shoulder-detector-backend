from django.urls import path
from . import views

app_name = 'examination'

urlpatterns = [
    path('upload/', views.detect_bone, name='detect_bone'),
    path('get/', views.ExaminationAPI.as_view(), name='examination_get'),
    path('list/', views.ExaminationAPI.as_view(), name='examination_list'),
    path('type/list/', views.ExaminationTypeAPI.as_view(), name='examination_type_list'),
]
