
from django.db import models
from django.contrib.auth.models import User


    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    batch = models.CharField(max_length=20, choices=[
        ('10A', '10A'), ('10B', '10B'), ('10C', '10C'), ('10D', '10D')
    ])
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)


