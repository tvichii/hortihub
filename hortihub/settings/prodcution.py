from .base import *
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = ['*','hortihub.herokuapp.com']


# Application definition
INSTALLED_APPS += (
    # other apps for production site
)

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Why?
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
STATICFILES_DIRS = [
    os.path.normpath(BASE_DIR, 'static'),
]

SOCIAL_AUTH_GITHUB_KEY = '5a1923402861bda4eb93'
SOCIAL_AUTH_GITHUB_SECRET = 'ce9ae60d506f24914b473cb05cbb12ef8803b41a'


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'