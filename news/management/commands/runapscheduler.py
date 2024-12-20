#  python manage.py runapscheduler
import datetime
import logging


from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives  #  D6
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string

from news.models import Post, Category, User

logger = logging.getLogger(__name__)


def my_job():
    # Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_created__gte=last_week)
    categories = set(posts.values_list('category__pk',
                                       flat=True)
                     )
    # flat=True - если не использовать, values_list вернёт список словарей,
    # где ключём будет category__category, а значением - название категории.
    # flat=True даст список строк без словаря

    # print(f'0______________________')
    # print(f'\n posts = {posts}')
    # print(f'\n categories = {categories}')
    # print(f'1______________________')
    # # subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    # # subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribers__email', flat=True))
    # print(f'User.objects.filter(subscriptions__category__in=categories) = {User.objects.filter(subscriptions__category__in=categories)}')
    # print(f"User.objects.filter(subscriptions__category__in=categories).values_list('email', flat=True) = {set(User.objects.filter(subscriptions__category__in=categories).values_list('email', flat=True))}")
    # print(f'2______________________')
    subscribers = set(User.objects.filter(subscriptions__category__in=categories).values_list('email', flat=True))
    html_content = render_to_string(
        'flatpages/daily_post.html',
        {
            'link': settings.SITE_URL,  # передаём просто домен -> все статьи
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',  # body описан в шаблоне
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')  # добавляем шаблон к html и формат шаблона
    msg.send()

# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            # trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00"
            ),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
