import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mobility.settings")

app = Celery("mobility")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'random_data': {
        'task': 'random_data',
        'schedule': 10,
        'args': ()
    }
}