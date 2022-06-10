from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Video, Category
from django.contrib import messages
from .forms import VideoForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def videos(request):
    videos = Video.objects.all()
    categories = Category.objects.all()
    form = VideoForm

    context = {
        'videos':videos,
        'categories':categories,
        'form':form
    }
    return render(request, 'videos/videos.html', context)

@login_required
def video_create(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return HttpResponseRedirect(reverse('videos:videos'))

    form = VideoForm()
    
    context = {
        'form':form
    }
    return render(request, 'videos/video_create.html', context)

def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if video.user == request.user:
        video.delete()
        return HttpResponseRedirect(reverse('videos:videos', kwargs={'pk':pk}))
    messages.error(request, 'you do not have permissions')
    return HttpResponseRedirect(reverse('videos:videos', kwargs={'pk':pk}))
    
