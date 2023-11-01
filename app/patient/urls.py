from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('list/', views.PatientAPI.as_view(), name='patient_list'),
    path('delete/', views.PatientAPI.as_view(), name='patient_delete'),
    path('create/', views.PatientAPI.as_view(), name='patient_create'),
]
