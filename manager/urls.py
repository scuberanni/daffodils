from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register_new/', views.register_new, name='register_new'),
    path('users-list/', views.users_list, name='users list'),
    path('gallery/', views.gallery, name='gallery'), 
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('edit/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
    path('teachers/', views.teachers, name='teachers'), 
    path('add-teacher/', views.add_teacher_profile, name='add_teacher_profile'),
    path('teacher/edit/<int:pk>/', views.edit_teacher_profile, name='edit_teacher_profile'),
    path('table/', views.table, name='table'),
    path('event/', views.event, name='event'),
    path('add_event/', views.add_event, name='add_event'),
    path('register_event/', views.register_event, name='register_event'),
    path('add_event_photo/', views.add_event_photo, name='add_event_photo'),
    path('photos/<int:pk>/', views.event_photos_detail, name='event_photos_detail'),
    path('photos/', views.photos, name='photos'),
    path('photos/<int:pk>/edit/', views.edit_event_photos, name='edit_event_photos'),
    path('photos/<int:pk>/delete/', views.delete_event_photos, name='delete_event_photos'),
    path('add_event_video/', views.add_event_video, name='add_event_video'),
    path('videos/', views.videos, name='videos'),
    path('video/<int:pk>/', views.event_video_detail, name='event_video_detail'),
    path('videos/<int:pk>/edit/', views.edit_event_video, name='edit_event_video'),
    path('videos/<int:pk>/delete/', views.delete_event_video, name='delete_event_video'),
]
