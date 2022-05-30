# from django.views.generic import CreateView
#
# from .forms import EmailForm
# from .models import Contact
# from .service import send
# from .tasks import send_spam_email




# class ContactView(CreateView):
#     model = Contact
#     form_class = EmailForm
#     success_url = '/'
#     template_name = 'contact.html'
#
#     def form_valid(self, form):
#         form.save()
#         send_spam_email.delay(form.instance.email)
#         return super().form_valid(form)
