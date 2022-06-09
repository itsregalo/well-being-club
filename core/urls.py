from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', IndexView, name='index'),
    path('contact/', ContactView, name='contact'),
]
