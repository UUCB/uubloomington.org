from .base import *
import os
import json
import sentry_sdk

DEBUG = False
with open(os.getenv("UUBLOOMINGTON_CONFIG_PATH")) as config_file:
    loaded_configuration = json.load(config_file)

STATIC_ROOT = loaded_configuration['static_root']

MEDIA_ROOT = loaded_configuration['media_root']

SECRET_KEY = loaded_configuration['secret_key']

PLANNING_CENTER_APPLICATION_ID = loaded_configuration['planning_center_app_id']
PLANNING_CENTER_SECRET = loaded_configuration['planning_center_secret']

ALLOWED_HOSTS = [host for host in loaded_configuration['allowed_hosts'].split(',')]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": loaded_configuration['mysql_config_path']
        },
    }
}

try:
    from .local import *
except ImportError:
    pass

sentry_sdk.init(
    dsn=loaded_configuration['sentry_dsn'],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
