from django import forms
from django.contrib.auth.models import User
from .models import EventPhoto

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


from .models import TeacherProfile

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['name', 'phone', 'address', 'batch', 'photo']
        widgets = {
            'batch': forms.Select(attrs={'class': 'form-control'}),
        }

class EventPhotoForm(forms.ModelForm):
    class Meta:
        model = EventPhoto
        fields = ['event', 'photo']
        labels = {
            'event': '',
            'photo': '',
        }