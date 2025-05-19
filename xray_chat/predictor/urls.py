from django.contrib import admin
from django.urls import path
from . import views  # Ensure this import is present
from django.core.exceptions import ValidationError
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('index', views.home, name='home'),

    path('register' , views.register , name = 'register') ,
    path('login', views.user_login, name='login'),
    path('logout', views.custom_logout, name='logout'),

    path('dashboard', views.dashboard, name='dashboard'),

    path('hand/', views.hand, name='hand'),
    path('leg/', views.leg, name='leg'),
    path('chest/', views.chest, name='chest'),

    path('chatbot_hand/', views.chatbot_api_hand, name="chatbot_api_hand"),
    path('chatbot_leg/', views.chatbot_api_leg, name="chatbot_leg"),
    path('chatbot_chest/', views.chatbot_api_chest, name="chatbot_api_chest"),
    
    path('upload_image_api_hand/', views.upload_image_api_hand, name='upload_image_api_hand'),
    path('upload_image_api_leg/', views.upload_image_api_leg, name='upload_image_api_leg'),
    path('upload_image_api_chest/', views.upload_image_api_chest, name='upload_image_api_chest'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)