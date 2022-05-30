from django.urls import path, include
from rest_framework import routers
from .api import ClientViewSet, NewsletterViewSet, MessageViewSet

router = routers.SimpleRouter()
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')
router.register(r'clients', ClientViewSet, basename='clients')
router.register(r'message', MessageViewSet, basename='message')

urlpatterns = [
    path('api/', include(router.urls)),
]
