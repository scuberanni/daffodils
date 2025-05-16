from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('approval-status/<str:username>/', views.approval_status, name='approval_status'),
     path('login/', views.user_login, name='user_login'),
     path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    
]
