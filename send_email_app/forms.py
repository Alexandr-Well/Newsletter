from django import forms

from .models import Contact


class EmailForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email']

