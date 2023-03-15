from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order_id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                Your order id is {}.'.format(order.first_name,
                                             order.id)
    mail_sent = send_mail(subject, message, 'katyushn@gmail.com', [order.email])
    return mail_sent


"""
Запуск ассинхронных задач для windows:
1. pip install celery
2. https://github.com/erlang/otp/releases/download/OTP-24.3.3/otp_win64_24.3.3.exe
3. https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.9.16/rabbitmq-server-3.9.16.exe 
4. pip install gevent
5. создать вайл celery.py как в этом проэкте
6. создать файл задач task.py
7. подключить celer в файле __init__.py в корневой дириктории
8. вызвать задачу в views.py
9. запустить в терминале в корневой дериктории из под виртуального окружения команду: celery -A projectname worker -l info -P gevent 
"""