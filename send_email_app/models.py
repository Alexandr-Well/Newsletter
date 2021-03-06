from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=40, blank=False, null=False)