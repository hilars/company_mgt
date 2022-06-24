
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView, DashboardView, EmployeeFormView, EmployeeView, get_employee_details, post_contract

urlpatterns = [
    path('backend/', admin.site.urls, name='Meters'),
    path('login/', LoginView.as_view(), name='Login'),
    path('dashboard/', DashboardView.as_view(), name='Dashboard'),
    path('employee/new', EmployeeFormView.as_view(), name='Add New Employee'),
    path('employee/all', EmployeeView.as_view(), name='Employees'),
    path('employee/<str:serial>', get_employee_details, name='Employee'),
    path('contract/<str:serial>/new', post_contract, name='Contract'),
]
