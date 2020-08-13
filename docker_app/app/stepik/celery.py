import os
import logging
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stepik.settings')

broker_service_host = os.getenv('RABBITMQ_SERVICE_SERVICE_HOST', 'localhost')
app = Celery('stepik', broker=f'pyamqp://guest@{broker_service_host}//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
logging.basicConfig(level=logging.INFO)
