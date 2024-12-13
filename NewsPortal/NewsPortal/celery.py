import os
from celery import Celery
from celery.schedules import crontab
# from NewsPortal.celery import Celery
# from NewsPortal.NewsPortal.celery import Celery
# from news.tasks import add


# from app.tasks import add




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {   #  celery D 7.4 11/11 Выполнение периодической задачи_ настройки
    # Executes every Monday morning at 08:00 a.m.
    'add-every-monday-morning': {
        'task': 'news.tasks.weekly_send_email_task',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # как часто повторять
    }
}

# app.conf.timezone = 'UTC'=

app.autodiscover_tasks()  # искать tasks автоматически, во всех приложениях
