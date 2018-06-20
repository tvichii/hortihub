from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3up3aw-a1n73oq7#^q!gy189zp4p@l7knldwl6y#nq!8e!7t(p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['example.com','http://example.com', '*', '127.0.0.1']

# Application definition

INSTALLED_APPS += (
    'debug_toolbar', # and other apps for local development
)
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Why?s

SOCIAL_AUTH_GITHUB_KEY = '5a1923402861bda4eb93'
SOCIAL_AUTH_GITHUB_SECRET = 'ce9ae60d506f24914b473cb05cbb12ef8803b41a'


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0