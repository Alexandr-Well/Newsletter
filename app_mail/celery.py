import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_mail.settings')

app = Celery('app_mail')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-email-every-day': {
        'task': 'mail_sender.tasks.send_email',
        'schedule': crontab(day_of_week='mon-fri'),
    },
}