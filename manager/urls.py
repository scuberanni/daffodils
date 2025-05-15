from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin',views.admin,name='admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register_new/', views.register_new, name='register_new'),
]
