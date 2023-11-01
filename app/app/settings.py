import os
from pathlib import Path
import django
from django.utils.encoding import force_str

django.utils.encoding.force_text = force_str

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')

DEBUG = bool(int(os.environ.get('DEBUG', 0)))

ALLOWED_HOSTS = ['localhost']
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(','),
    )
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'core',
    'user',
    'django_oss_storage',
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:5173",
    "http://localhost:8081",
    "http://121.5.47.2:4000",
    "http://localhost:4080",
    "http://127.0.0.1:4080",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:3050",
    "http://127.0.0.1:3050",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'core.User'

EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "549288160@qq.com"
EMAIL_HOST_PASSWORD = "mbmjsjetruhnbdfg"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True

LANGUAGE_CODE = 'en-us'
USE_I18N = True
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

DEFAULT_FILE_STORAGE = 'django_oss_storage.backends.OssMediaStorage'
OSS_ACCESS_KEY_ID = 'LTAI5tH3N9bs5veG3cn84pNR'
OSS_ACCESS_KEY_SECRET = 'LusobjZXgYqPptpawKOJGP46VRF5c3'
OSS_BUCKET_NAME = 'shoulder'
OSS_ENDPOINT = 'oss-accelerate.aliyuncs.com'


MEDIA_URL = 'media/'
STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR / 'media/'
