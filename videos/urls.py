from django.urls import path
from .views import *

app_name = 'videos'

urlpatterns = [
    path('', index, name='index'),
]
