from .base import *  # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea',
        'PASSWORD': '123456',
        'USER': 'learn',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}