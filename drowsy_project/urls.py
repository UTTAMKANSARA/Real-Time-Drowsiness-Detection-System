from django.contrib import admin
from django.urls import path
from detection import views as detection_views # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),

    
    path('', detection_views.index, name='home'),
    path('video_stream/', detection_views.stream, name='video_stream'), 
]