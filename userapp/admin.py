from django.contrib import admin
from .models import UserProfile, TeacherProfile, events, EventPhoto, EventVideo

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'user', 'phone', 'batch', 'is_approved')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'
admin.site.register(TeacherProfile)
admin.site.register(events)
admin.site.register(EventPhoto)
admin.site.register(EventVideo)
