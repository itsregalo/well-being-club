from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import ContactForm, EmailSubscriberForm
from django.core.mail import send_mail

from videos.models import Video
from blog.models import Blog
from tips.models import Tip

def IndexView(request, *args, **kwargs):
    # latest 8 videos
    videos = Video.objects.all().order_by('-date_added')[:8]
    blogs = Blog.objects.all().order_by('-pub_date')[:3]
    tips = Tip.objects.all().order_by('-pub_date')[:3]
    context = {
        'latest_blogs': blogs,
        'latest_videos': videos,
        'latest_tips': tips,
        'subscribe_form': EmailSubscriberForm(),
    }
    return render(request, 'index.html', context)

def AboutUsView(request, *args, **kwargs):
    return render(request, 'about-us.html')

def FAQView(request, *args, **kwargs):
    return render(request, 'faq.html')


def ContactView(request, *args, **kwargs):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, email, ['yourmail.com'])
            return HttpResponseRedirect(reverse('core:index'))

    context = {
        'form': form
    }

    return render(request, 'contact.html', context)

def EmailSubscriberView(request, *args, **kwargs):
    form = EmailSubscriberForm()
    if request.method == 'POST':
        form = EmailSubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_mail('Email Subscription', 'You have been successfully subscribed to our email list', ' yourmail.com', [email])
            form.save()
            return HttpResponseRedirect(reverse('core:index'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
def error_404(request, exception):
    return render(request, '404.html')

def error_500(request):
    return render(request, '500.html')

