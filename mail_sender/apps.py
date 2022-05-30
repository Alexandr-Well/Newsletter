from django.apps import AppConfig
from django.core.signals import request_finished


class MailSenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mail_sender'

    def ready(self):
        from .service import signals
        # request_finished.connect(signals.newsletter_callback)
