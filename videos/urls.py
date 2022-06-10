from django.urls import path
from .views import *

app_name = 'videos'

urlpatterns = [
    path('', videos, name='videos'),
    path('<int:video_id>/delete/', video_delete, name='video'),
    path('video-create/', video_create, name='video-create'),
    
]
