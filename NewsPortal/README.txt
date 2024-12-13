
D7.5
Задание 6.7.1 (HW-03)
1. Redis установлен
2. Celery установлен
3. settings.py дополнен настройками CELERY
4. Рассылка уведомлений после создания новостей реалзована tasks.send_email_task. 
Который получает запускается сигналом notify_about_new_post.
5. Еженедельная рассылка реализована через tasks.weekly_send_email_task