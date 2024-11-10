from django.urls import path
from . import views

app_name = 'designapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.ApplicationListView.as_view(), name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]

urlpatterns += [
    path('create', views.create_application, name='application-create'),
    path('application/<int:application_id>/delete/', views.delete_application, name='application-delete'),
]