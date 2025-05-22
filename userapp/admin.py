from django.contrib import admin
from .models import UserProfile, TeacherProfile, events, EventPhoto, EventVideo

admin.site.register(UserProfile)
admin.site.register(TeacherProfile)
admin.site.register(events)
admin.site.register(EventPhoto)
admin.site.register(EventVideo)
