from .base import *
import os
import sentry_sdk

DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECRET_KEY = os.environ['SECRET_KEY']

PLANNING_CENTER_APPLICATION_ID = os.environ['PLANNING_CENTER_APPLICATION_ID']
PLANNING_CENTER_SECRET = os.environ['PLANNING_CENTER_SECRET']

ALLOWED_HOSTS = [os.environ['VIRTUAL_HOST']]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ['DB_HOST'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'OPTIONS': {
            'ssl': {},
            'charset': 'utf8mb4',
        },
    }
}

try:
    from .local import *
except ImportError:
    pass

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
SERVER_EMAIL = os.environ['SERVER_FROM_EMAIL']

ANYMAIL = {
    "SENDGRID_API_KEY": os.environ['SENDGRID_API_KEY']
}
