from django.urls import path
from . import views


urlpatterns = [
    path('register_book/', views.register_book, name='register_book'),
    path('register/', views.register, name='register'),
    path('approval-status/<str:username>/', views.approval_status, name='approval_status'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.view_profile, name='view_profile'),
    path('edit_user/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('student/<int:profile_id>/', views.user_detail, name='user_detail'),
    path('teacher/<int:profile_id>/', views.teacher_detail, name='teacher_detail'),
    path('all_teachers/', views.all_teachers, name='all_teachers'), 
    path('class_a/', views.user_class_a, name='class_a'),
    path('class_b/', views.user_class_b, name='class_b'),
    path('class_c/', views.user_class_c, name='class_c'),
    path('class_d/', views.user_class_d, name='class_d'),
    path('view_gallery/', views.view_gallery, name='view_gallery'), 
    path('view_event/', views.view_event, name='view_event'), 
    path('view_photos/', views.view_photos, name='view_photos'),
    path('view_photos/<int:pk>/', views.view_event_photos_detail, name='view_event_photos_detail'),
      
    path('view_videos/', views.view_videos, name='view_videos'), 
    path('view_video/<int:pk>/', views.view_event_video_detail, name='view_event_video_detail'),
    path('view_videos/<int:pk>/', views.view_event_video_details, name='view_event_video_details'),
    path('view_photo/<int:pk>/', views.view_event_photos_details, name='view_event_photos_details'),
    path('view_event_detail/<int:pk>/', views.view_event_detail, name='view_event_detail'), 
    path('view_photos_event/<str:event_name>/', views.view_photos_event, name='view_photos_event'),
    path('view_videos_event/<str:event_name>/', views.view_videos_event, name='view_videos_event'),



    
]
