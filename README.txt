D6.7
Задание 6.7.1 (HW-03)


1. часть
- подписки на рассылку: http://127.0.0.1:8000/subscriptions/
- создана модель Subscription (вместо Subscriber);
- создан сигнал notify_about_new_post;


2. часть (отправка статей чарез промежуточную модель Subscription; ...related_name='subscriptions',)
- django_apscheduler
- ..\news\management\commands\runapscheduler.py
- команда запуска периодических задач my_job;
- day_of_week="fri", hour="18", minute="00";
- сообщение со ссылками на статьи: flatpages/daily_post.html;
- posts = Post.objects.filter(time_created__gte=last_week).
