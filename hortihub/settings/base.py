"""
Base settings to build other settings files upon.
"""

import os
from django.urls import reverse_lazy
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

DEBUG = config('DEBUG', cast=bool)
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '3up3aw-a1n73oq7#^q!gy189zp4p@l7knldwl6y#nq!8e!7t(p'
SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = ['example.com','http://example.com', '*', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'channels',
    'widget_tweaks',
    'avatar',
    'social_django',
    'rest_framework',
    'accounts',
    'feed',
    'hortihome',
    'actions',
    'notifications',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.login_middleware.LoginRequiredMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'hortihub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'hortihub.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# REDIS setup
REDIS_URL = config('REDIS_URL', default=('localhost', 6379))

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgi_redis.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [REDIS_URL,],
#         },
#         "ROUTING": "notifications.routing.channel_routing",
#     },
# }

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Why?


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOGIN_EXEMPT_URLS = (
 r'^/accounts/login/$',
 r'^accounts/logout/$',
 r'^accounts/signup/$',
 r'^oauth/',
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/feed/userfeed/'
LOGOUT_REDIRECT_URL = '/'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('accounts:userdetail', args=[u.pk])
}

INTERNAL_IPS = ['127.0.0.1',]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication.EmailAuthBackend',
)

SOCIAL_AUTH_GITHUB_KEY = '5a1923402861bda4eb93'
SOCIAL_AUTH_GITHUB_SECRET = 'ce9ae60d506f24914b473cb05cbb12ef8803b41a'

SOCIAL_AUTH_FACEBOOK_KEY = '465322103890630'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '9cf27fb32b2725b613cc096b3d1d85ed'  # App Secret


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0