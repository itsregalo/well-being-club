from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', IndexView, name='index'),
    path('contact/', ContactView, name='contact'),
    path('faq/', FAQView, name='faqs'),
    path('about-us/', AboutUsView, name='about-us'),
    path('email-subscriber/', EmailSubscriberView, name='email-subscriber'),
]
