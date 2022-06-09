from django.shortcuts import render
from .models import *

def courses(request, *args, **kwargs):
    courses = Course.objects.all()

    context = {
        'courses': courses
    }
    return render(request, "courses/courses.html",context)