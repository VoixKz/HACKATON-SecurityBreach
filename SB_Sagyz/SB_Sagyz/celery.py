# SB_Sagyz/SB_Sagyz/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SB_Sagyz.settings')

app = Celery('SB_Sagyz')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()