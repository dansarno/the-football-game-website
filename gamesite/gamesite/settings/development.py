from .base import *
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


DEBUG = True

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': os.getenv("DB_NAME"),
    #     'USER': os.getenv("DB_USER"),
    #     'PASSWORD': os.getenv("DB_PASSWORD"),
    #     'HOST': os.getenv("DB_HOST"),
    #     'PORT': "",  # os.getenv("DB_POST"),
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE
 
INSTALLED_APPS += [
        'debug_toolbar',
    ]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: False,  # disables it
    # '...
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
