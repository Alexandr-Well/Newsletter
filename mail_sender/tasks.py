import os

from dotenv import load_dotenv
import datetime
from typing import Dict, List
import requests
from django.core.mail import send_mail
from django.db import transaction
from .models import Message, Newsletter
from app_mail.celery import app


load_dotenv()
URL = 'https://probe.fbrq.cloud/v1/send/'
TOKEN = os.getenv("TOKEN")

header = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'}


def do_msg(msg: List, obj: List, news: Dict, queryset: Dict, url: str) -> None:
    """
    Вспомогательная ф-ия для send_message(убирает дублирование кода)
    :param obj: error message list ссылка на errors_msg из send_message()
    :param msg: неудачные обьекты рассылки ссылка на errors_obj из send_message()
    :param queryset: объекты сообщения в виде словаря:
    :param news: обьект Newsletter в виде словаря(не все поля только id и текст)
    :param url: адрес стороннего api
    """
    for message in queryset:
        data = {
            'id': message['message']['id'],
            "phone": message['client'],
            "text": news['text']
        }
        with transaction.atomic():
            try:
                requests.post(url=url + str(message['message']['id']), headers=header, json=data)
                message = Message.objects.only('status').get(pk=message['message']['id'])
                message.status = True
                message.save()
            except requests.exceptions.RequestException as exc:
                obj.append(data)
                msg.append(exc)


@app.task(bind=True, retry_backoff=True)
def send_message(self, queryset: Dict, news: Dict, url: str = URL) -> None:
    """
    таск принемает парраметры и запускает рассылку,
    :param queryset: объекты сообщения в виде словаря:
    :param news: обьект Newsletter в виде словаря(не все поля только id и текст)
    :param url: адрес стороннего api
    :return: None
    """
    errors_obj = []
    errors_msg = []
    retries = 10
    connection_try = 0
    while connection_try < retries:
        if not errors_obj:
            do_msg(errors_msg, errors_obj, news, queryset, url)
        connection_try += 1
        if not errors_obj:
            break
        queryset = errors_obj[:]
        errors_obj.clear()
        do_msg(errors_msg, errors_obj, news, queryset, url) # нужно подправить


@app.task
def send_email():
    """
    таск отправляет письмо на указанную почту
    :return:
    """
    # можно пробросить почту из settings
    current_date = datetime.datetime.today().strftime('%Y-%m-%d') + "T00:00:00Z"
    data = Newsletter.objects.filter(start_date__gte=current_date)

    text_view = []
    for object in data:
        text_view.append(
            f"task id: {object.pk},"
            f"start: {object.start_date},"
            f" end: {object.end_date}, "
            f"code: {object.mobile_code}, "
            f"text: {object.text}, "
            f"tag: {object.tag},"
            f"send: {object.to_send}")

    msg_body = "\n".join(text_view)
    send_mail(
        "test",
        msg_body,
        "test@gmail.com", # подставить нужную почту
        ['test@mail.ru'], # подставить нужную почту
        fail_silently=False
    )
