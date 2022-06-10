from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Video, Category
from django.contrib import messages
# Create your views here.

def videos(request):
    videos = Video.objects.all()
    categories = Category.objects.all()

    context = {
        'videos':videos,
        'categories':categories
    }
    return render(request, 'videos/videos.html', context)

def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if video.user == request.user:
        video.delete()
        return HttpResponseRedirect(reverse('videos:videos', kwargs={'pk':pk}))
    messages.error(request, 'you do not have permissions')
    return HttpResponseRedirect(reverse('videos:videos', kwargs={'pk':pk}))
    
