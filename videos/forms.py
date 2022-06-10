from django import forms
from matplotlib import widgets

from .models import Video, Category

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'category', 'youtube_link']

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control mb-2'}),
            'youtube_link': forms.TextInput(attrs={'class':'form-control'}),
        }