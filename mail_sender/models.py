from django.db import models
from django.utils import timezone
import pytz

TIMEZONES = list(zip(pytz.all_timezones, pytz.all_timezones))


class Newsletter(models.Model):
    """
    Модель Рассылки
    """

    start_date = models.DateTimeField('start')
    end_date = models.DateTimeField('end')
    text = models.TextField('message', max_length=300, null=False, blank=False)
    tag = models.CharField('tag', max_length=50, blank=True, null=True)
    mobile_code = models.CharField('mobile code', max_length=3, blank=True, null=True)

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletter'

    @property
    def to_send(self):
        if self.start_date <= timezone.now() < self.end_date:
            return True
        return False

    def __str__(self):
        return f'Newsletter №: {self.pk} started: {self.start_date}, ended: {self.end_date}'


class Client(models.Model):
    """
    Модель клиента
    """
    # предпологаю валидация номера на фронте
    email = models.EmailField('email', unique=True, blank=True, )
    phone = models.CharField('phone', max_length=11, blank=True, null=True)
    mobile_code = models.CharField('mobile code', editable=False, max_length=3)
    tag = models.CharField('tag', max_length=50, blank=True)
    timezone = models.CharField('time zone', max_length=32, choices=TIMEZONES, default='UTC')

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Client'

    def save(self, *args, **kwargs):
        self.mobile_code = self.phone[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'Client number: {self.phone}'


class Message(models.Model):
    """
        Модель сообщения
    """
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    status = models.BooleanField('send', default=False)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Message'

    def __str__(self):
        return f'Message: {self.pk} text: {self.newsletter} client: {self.client}'
