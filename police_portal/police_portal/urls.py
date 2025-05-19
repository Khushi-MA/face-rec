"""
URL configuration for police_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.user_dashboard, name='user_dashboard')
Class-based views
    1. Add an import:  from other_app.views import User_dashboard
    2. Add a URL to urlpatterns:  path('', User_dashboard.as_view(), name='user_dashboard')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('system.urls')),  # system is your app name
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
