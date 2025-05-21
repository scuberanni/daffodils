from django import forms
from django.contrib.auth.models import User
from .models import EventPhoto,EventVideo

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

class EventVideoForm(forms.ModelForm):
    class Meta:
        model = EventVideo
        fields = ['event', 'video']
        labels = {
            'event': '',
            'video': '',
        }
        widgets = {
            'event': forms.Select(attrs={'class': 'form-select'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

def clean_video(self):
        video = self.cleaned_data.get('video')
        if video and video.size > 10 * 1024 * 1024:  # 10 MB limit (example)
            raise forms.ValidationError("Video file must be under 10MB.")
        return video