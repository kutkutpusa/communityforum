from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from forum.models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class PasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        widgets = {
          'reply': forms.Textarea(attrs={'rows':3, 'cols':110}),
        }
        fields = ['reply']