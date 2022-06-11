from django.urls import path
from .views import *

app_name = 'memes'

urlpatterns = [
    path('', memes, name='memes'),
    path('<int:id>/delete/', meme_delete, name='meme-delete'),
]
