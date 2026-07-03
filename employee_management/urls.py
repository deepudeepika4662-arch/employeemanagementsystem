from django.contrib import admin
from django.urls import path, include
from employees import views as emp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', emp_views.home, name='home'),
    path('employees/', include('employees.urls')),
]
