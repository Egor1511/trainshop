from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ {order.id}'
    message = f'{order.first_name},\n\nВы успешно разместили заказ. Ваш номер заказа №{order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'egoriegor1511@gmail.com',
                          [order.email])
    return mail_sent
