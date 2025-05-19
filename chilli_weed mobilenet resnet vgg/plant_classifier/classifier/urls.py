from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from . import views 
urlpatterns = [

    path('', views.classify_image, name='classify_image'),

]
