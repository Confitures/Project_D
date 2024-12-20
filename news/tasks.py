# from project import shared_task
# from celery import app_task
import time

# from celery import app
# from NewsPortal.celery import app
from NewsPortal.celery import app
# from NewsPortal.celery import shared_task

import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from celery import shared_task

from NewsPortal import settings
from NewsPortal.settings import SITE_URL

from news.models import Post, Category, User, PostCategory


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        # render_to_string() берёт за основу шаблон и использует его в качестве письма пользователю
        'flatpages/post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/newsportal/news/{pk}'
        }
    )

    for i in subscribers:
        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[i],  #  откорректировать тип данных
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def send_email_task(post_id: int):
    post = Post.objects.get(pk=post_id)

    categories = post.category.all()
    subscribers: list[str] = []
    for category in categories:
        # subscribers += category.subscribers.all()
        # subscribers += category.subscribers.all()
        subscribers += User.objects.filter(subscriptions__category=category)
    subscribers = [s.email for s in subscribers]
    send_notifications(post.preview(), post.pk, post.title, subscribers)

    # _________________________

@shared_task
def weekly_send_email_task():
    print(f'START weekly_send_email_task')
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=207)
    posts = Post.objects.filter(time_created__gte=last_week)
    categories = set(posts.values_list('category__pk',
                                       flat=True)
                     )
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
    msg.send()   #  or through send_notifications()
    print(f'END weekly_send_email_task')

