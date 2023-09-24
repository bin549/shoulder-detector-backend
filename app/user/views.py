from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.sites.shortcuts import get_current_site
from utils.captcha.sdcaptcha import Captcha
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db.models import Q

from core.models import (
    User,
)
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)
from utils import (
    restful
)

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



def email_captcha(request):
    to_email = request.GET.get('email')
    is_register = request.GET.get('is_register')
    if len(User.objects.filter(Q(email=to_email))) != 0 and is_register:
        return restful.params_error(message="该邮箱已被注册！")
    mail_subject = 'STEM邮箱验证'
    current_site = get_current_site(request)
    code = Captcha.gene_text()
    message = render_to_string('accounts/account_verification_email.html', {
            'domain': current_site,
            # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            # 'token': default_token_generator.make_token(user),
            'code': code,
        })
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    return HttpResponse(int(code))

