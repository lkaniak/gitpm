from .base_settings import *
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
DEBUG = True
SECRET_KEY = '1nw&8^!2h0o)7dfgk=(xot_n^x5lv3wgu6gvzey#6k+=27e*l*'

INSTALLED_APPS.append('corsheaders')
MIDDLEWARE.extend(['corsheaders.middleware.CorsMiddleware',
'django.middleware.common.CommonMiddleware'])

CORS_ORIGIN_ALLOW_ALL = True

CORS_EXPOSE_HEADERS = ['Content-Disposition']

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'Content-Disposition',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'referer',
    'session',
    'x-credentials',
    'x-token',
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
)
