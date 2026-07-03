from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='list'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add/', views.employee_create, name='add'),
    path('detail/<int:pk>/', views.employee_detail, name='detail'),
    path('edit/<int:pk>/', views.employee_update, name='edit'),
    path('delete/<int:pk>/', views.employee_delete, name='delete'),
    path('cbv/', views.EmployeeListView.as_view(), name='cbv'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
