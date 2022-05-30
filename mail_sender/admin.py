from django.contrib import admin

from .models import Newsletter, Client, Message


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):

    pass


@admin.register(Client)
class NewsletterAdmin(admin.ModelAdmin):

    pass


@admin.register(Message)
class NewsletterAdmin(admin.ModelAdmin):

    pass
