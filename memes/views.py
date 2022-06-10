from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import MemeForm
# Create your views here.

def memes(request):
    form = MemeForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = MemeForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('memes'))
    memes = Meme.objects.all()
    context = {
        'memes': memes,
        'form': form,
    }
    return render(request, 'memes/memes.html', context)

def meme_delete(request, id):
    meme = Meme.objects.get(id=id)
    if request.user == meme.user:
        meme.delete()
    return HttpResponseRedirect(reverse('memes'))