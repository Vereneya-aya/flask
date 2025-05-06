from celery import Celery
from celery.schedules import crontab

def make_celery(app_name=__name__):
    celery = Celery(
        app_name,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )
    celery.conf.update(
        timezone='UTC',
        enable_utc=True,
        beat_schedule={
            'send-weekly-newsletter': {
                'task': 'tasks.send_newsletter',
                'schedule': crontab(minute=0, hour=9, day_of_week=0),
            }
        }
    )
    return celery

celery = make_celery()