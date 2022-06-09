from django.shortcuts import render
from .models import *

def IndexView(request):
    return render(request, 'courses/index.html')