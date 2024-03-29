from django.urls import (
    path,
)
from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('email_captcha/', views.email_captcha, name='email_captcha'),
]