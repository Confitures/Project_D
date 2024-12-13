# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives  # D6
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
# from django.template.loader import render_to_string
# from allauth.account.signals import user_signed_up  # D6





from .models import PostCategory, Subscription
from .tasks import send_email_task





@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        # print(f'instance = {instance}; type(instance) = {type(instance)}')
        # print(f'instance.category.all() = {instance.category.all()}')
        send_email_task.apply_async([instance.pk])
