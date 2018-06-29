from .base import *
from decouple import config

ALLOWED_HOSTS = ['*', '127.0.0.1']

# Application definition
INSTALLED_APPS += (
    'debug_toolbar', # and other apps for local development
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, config("DB_NAME")),
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Why?s

# ASGI_APPLICATION = 'chatapp.routing.application'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
