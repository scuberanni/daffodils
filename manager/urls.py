from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register_new/', views.register_new, name='register_new'),
    path('users-list/', views.users_list, name='users list'),
    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('edit/<int:user_id>/', views.edit_user_profile, name='edit_user_profile'),
]
