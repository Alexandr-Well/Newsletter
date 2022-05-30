from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from .models import Newsletter, Client, Message
from .paginators import CommonPagination
from .serializers import NewsletterSerializer, ClientSerializer, MessageSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
        Сермалайзер модели клиента
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    pagination_class = CommonPagination


class MessageViewSet(viewsets.ModelViewSet):
    """
        Сермалайзер модели сообщения
    """
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    pagination_class = CommonPagination


class NewsletterViewSet(viewsets.ModelViewSet):
    """
    Сермалайзер модели рассылки
    """
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    # pagination_class = CommonPagination

    @action(detail=True, methods=['get'])
    def message_info(self, request, pk=None):
        """
        Детализация сообщения
        """
        queryset = Message.objects.filter(newsletter_id=pk).all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def newsletter_info(self, request):
        """
        Детализация рассылки
        """
        send_msg = Newsletter.objects.filter(message__status=True).annotate(snd_msg=Count("message__pk"))
        all_msg = Newsletter.objects.all().annotate(all_msg=Count("message__pk"))
        context = {'Mailings': len(all_msg)}
        context_temp_data = {}
        # мне не нравиться вариант с двумя циклами, но я пока не могу быстро понять правильную агрегацию для данных
        for mail in all_msg:
            context_temp_data[mail.pk] = {"all msg": mail.all_msg, 'send': 0, "fail": mail.all_msg}
        for mail in send_msg:
            context_temp_data[mail.pk]['send'] = mail.snd_msg
            context_temp_data[mail.pk]['fail'] = context_temp_data[mail.pk]['all msg'] - mail.snd_msg

        context['full mailing info'] = context_temp_data
        return Response(context)
