from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from src.settings.constants import ENV


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', ENV)
app = Celery('src')

CELERY_TIMEZONE = 'UTC'

# Using a string here means the worker will not have to
# pickle the object when using Windows.

app.config_from_object('django.conf:settings')

app.conf.broker_transport_options = {'visibility_timeout': 43600,
                                     'fanout_prefix': True,
                                     'fanout_patterns': True,
                                     }

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
