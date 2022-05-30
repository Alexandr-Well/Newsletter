import datetime
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from ..tasks import send_message
from ..models import Newsletter, Client, Message


@receiver(post_save, sender=Newsletter, dispatch_uid="newsletter_callback")
def newsletter_callback(sender, instance, **kwargs) -> None:
    """
    сигнал срабатывающий при сохранении модели рассылки, сразу же пытается отправить таск в селери
    :param instance : Newsletter -instance
    :return: None
    """

    clients = Client.objects.filter(Q(mobile_code=instance.mobile_code) |
                                    Q(tag=instance.tag)).all()
    queryset = []

    with transaction.atomic():
        for client in clients:
            message = Message.objects.create(
                status=False,
                client_id=client.id,
                newsletter_id=instance.id
            )
            message.save()
            queryset.append({'message': {"id": message.pk, }, 'client': client.phone})
    news = {'id': instance.id, 'text': instance.text}
    if instance.to_send:
        send_message.apply_async((queryset, news), expires=instance.end_date, countdown=5)
    else:
        fulldate_start_day = datetime.datetime.strptime(str(instance.start_date)[:-6],
                                                        "%Y-%m-%d %H:%M:%S") + datetime.timedelta(milliseconds=1)
        delay = fulldate_start_day - datetime.datetime.utcnow()
        delay = int(delay.total_seconds()) + 1
        send_message.apply_async((queryset, news), expires=instance.end_date, countdown=delay)
