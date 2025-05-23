from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classifier.urls')),  # Add this line

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)