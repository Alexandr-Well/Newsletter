from rest_framework import serializers
from .models import Newsletter, Client, Message


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('start_date',
                  'end_date',
                  'text',
                  'tag',
                  'mobile_code',
                  )


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('phone',
                  'email',
                  'mobile_code',
                  'tag',
                  'timezone',
                  )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('created_at',
                  'status',
                  'newsletter',
                  'client',
                  )
