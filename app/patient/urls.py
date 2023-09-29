from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('list/', views.PatientAPI.as_view()),
]
