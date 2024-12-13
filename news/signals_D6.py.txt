from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives  #  D6
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up   #  D6

from NewsPortal import settings
# from NewsPortal.settings import SITE_URL

from .models import PostCategory, Subscription


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(  #  render_to_string() берёт за основу шаблон и использует его в качестве письма пользователю
        'post_created_email.html',
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
            to=i,
        )
        msg.attach.alternative(html_content, 'text/html')
        msg.send()



# @receiver(m2m_changed, sender=PostCategory)
# def news_created(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add' and instance.item == 'news':  #  оповещение об новостях
#         print(f'Создан пост?_!{instance.item}', instance)
#         print(f'instance  ={instance}!!!')
#
#         subscribers = User.underscore(subscriptions__category=instance.category).values_list('email', flat=True)
#
#         print(f'Создан пост?_!{instance.item}', instance)
#         print(f'instance  ={instance}!!!')
#
#         ## __________________________________
#         # categories = instance.category.all()
#         # subscribers: list[str] = []
#         # for i in categories:
#         #     subscribers += categories.all()
#         #
#         # subscribers = [s.email for s in subscribers]
#
#         # send_notifications(instance.preview(), instance.pk, instance.title, subscribers)
#         ## __________________________________
#
#
#     # # print(f'Создан пост?_!{instance.item}', instance)
#     # print(f'Создан пост?_!{instance.item}', instance)



@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
#  Семинар 9/13  (sender - неименнованный аргумент;
# instance - объект модели в сигнале; **kwargs - именнованные аргументы)
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()   #  но категория у новости всегда одна!
        subscribers: list[str] = []
        for category in categories:
            # subscribers += category.subscribers.all()
            subscribers += User.objects.filter(subscriptions__category=category)

        subscribers = [s.email for s in subscribers]
        # # test____________________________
        # print(f'signal_signal_signal!!!'
        #       f'\n notify_about_new_post; '
        #       f'\n instance.preview() = {instance.preview()}; '
        #       f'\n instance.pk {instance.pk}; '
        #       f'\n instance.title = {instance.title};'
        #       f'\n subscribers = {subscribers};'
        #       f'\n ___________________________')
        # # test____________________________
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)





# #_________________________________________

# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
# #  Семинар 9/13  (sender - неименнованный аргумент;
# # instance - объект модели в сигнале; **kwargs - именнованные аргументы)
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers: list[str] = []
#         for category in categories:
#             # subscribers += category.subscribers.all()
#             subscribers += category.subscribers.all()
#
#         subscribers = [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

# #_________________________________________

from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import Product
#
#
# @receiver(post_save, sender=Product)
# def product_created(instance, **kwargs):
#     print('Создан товар', instance)



# #_________________________________________
#
# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import Post
#
#
# @receiver(m2m_changed, sender=Product)
# def product_created(instance, created, **kwargs):
#     # print('Создан товар', instance)
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.category
#     ).values_list('email', flat=True)
#
#     subject = f'Новый товар в категории {instance.category}'
#
#     text_content = (
#         f'Товар: {instance.name}\n'
#         f'Цена: {instance.price}\n\n'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на товар</a>'
#     )
#
#     html_content = (
#         f'Товар: {instance.name}<br>'
#         f'Цена: {instance.price}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на товар</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()