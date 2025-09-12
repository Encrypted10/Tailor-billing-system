"""
URL configuration for billing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from billapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('update_status/', views.update_status, name='update_status'),
    path('success', views.successpage, name='success'),
    path('details', views.details, name='details'),
    path('delete_record/<int:record_id>/',views.delete_record,  name='delete_record'),
    path('tailoring_form_view/', views.tailoring_form_view, name='tailoring_form_view'),
    path('generate_pdf/', views.generate_pdf_view, name='generate_pdf'),
    path('tailoring_list/', views.tailoring_list, name='tailoring_list'), # List of all tailoring records
    path('edit/<int:pk>/', views.edit_tailoring, name='edit_tailoring'),
    path('tailoring/<int:pk>/', views.tailoring_detail, name='tailoring_detail'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),



]
