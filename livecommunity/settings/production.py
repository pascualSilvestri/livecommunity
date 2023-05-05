from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['livecommunity.com','localhost']
CSRF_TRUSTED_ORIGINS = ['https://livecommunity.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'livecommunity',
        'USER': 'root',
        'PASSWORD': 'livecommunity01',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}