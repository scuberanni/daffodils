
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True ,default='+91')
    batch = models.CharField(max_length=20, choices=[
        ('10A', '10A'), ('10B', '10B'), ('10C', '10C'), ('10D', '10D')
    ])
    n_adult = models.PositiveIntegerField(null=True, blank=True, default=0)
    n_child = models.PositiveIntegerField(null=True, blank=True , default=0)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    is_approved = models.BooleanField(default=False)

class TeacherProfile(models.Model):
    name = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15, default='+91')
    address = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=20, blank=True, null=True)
    batch = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('10A', '10A'), ('10B', '10B'), ('10C', '10C'),
            ('10D', '10D'), ('Other', 'Other')
        ]
    )
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

class events(models.Model):
    name = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class EventPhoto(models.Model):
    updated_date = models.DateTimeField(default=timezone.now)
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='event_photos/')

    def __str__(self):
        return f"{self.event.name} - {self.updated_date.strftime('%Y-%m-%d %H:%M')}"
    
class EventVideo(models.Model):
    updated_date = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    video = models.FileField(upload_to='event_videos/')

    def __str__(self):
        return f"{self.event.name} - {self.updated_date.strftime('%Y-%m-%d %H:%M')}"



