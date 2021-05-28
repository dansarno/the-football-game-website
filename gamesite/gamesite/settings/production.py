from .base import *
import os
from dotenv import load_dotenv

load_dotenv()


DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': "",  # os.getenv("DB_POST"),
    }
}


# SMTP Configuration

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = ''
# EMAIL_PORT = ''
# EMAIL_USE_TLS = ''
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''


# Cache
# https://docs.djangoproject.com/en/3.1/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': r'/Users/danielsarno/Documents/the-football-game-website/gamesite',
        'TIMEOUT': None,
    }
}

SECURE_SSL_REDIRECT=True
