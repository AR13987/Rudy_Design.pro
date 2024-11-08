from django.urls import path
from . import views
from .views import register

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.ApplicationListView.as_view(), name='profile'),
    path('register/', register, name='register'),
    path('login/', views.login_view, name='login'),
]