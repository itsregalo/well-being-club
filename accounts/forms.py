from django import forms
from .models import *
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 
                                                            'placeholder': 'Username'}))
    password = forms.CharField(max_length=100, 
                    widget=forms.PasswordInput(attrs={'class': 'form-control', 
                                                    'placeholder': 'Password'}))

    fields = ['username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Invalid username or password')
        return cleaned_data


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    fields = ['username', 'email', 'password', 'confirm_password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password')
        )
        user.save()
        return user



