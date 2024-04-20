"""
URL configuration for Car_Renting_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# Importing required modules from Django
from django.contrib import admin  # Module for Django admin interface
from django.urls import path, include  # Module for defining URL patterns
from django.conf import settings  # Module for accessing project settings
from django.conf.urls.static import static  # Module for serving static files during development

# URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # URL pattern for accessing Django admin interface
    path('accounts/', include('allauth.urls')),  # URL pattern for user authentication
    path('user/', include('users.urls')),  # URL pattern for user-related functionalities
    path('rent/', include('rent.urls')),  # URL pattern for rent-related functionalities
    path('ckeditor/', include("ckeditor_uploader.urls")),  # URL pattern for CKEditor file uploader
    path('', include("core.urls")),  # URL pattern for core functionalities
]

# Adding URL patterns for serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
