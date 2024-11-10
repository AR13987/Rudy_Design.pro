from django.urls import path
from . import views

app_name = 'designapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.ApplicationListView.as_view(), name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('admin_profile/', views.AdminProfileView.as_view(), name='admin-profile'),
]

urlpatterns += [
    path('create', views.create_application, name='application-create'),
    path('application/<int:application_id>/delete/', views.delete_application, name='application-delete'),
]

urlpatterns += [
    path('admin_categories/', views.CategoryListView.as_view(), name='admin-category-list'),
    path('admin_categories_add/', views.CategoryCreateView.as_view(), name='admin-category-add'),
    path('admin_categories_delete/<int:category_id>/', views.CategoryDeleteView.as_view(), name='admin-category-delete'),
    path('admin_change_status/<int:application_id>/', views.ChangeStatusView.as_view(), name='change-status'),
]