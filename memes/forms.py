from django import forms

from .models import Meme

class MemeForm(forms.Model):
    class Meta:
        model = Meme
        fields = ['title', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }